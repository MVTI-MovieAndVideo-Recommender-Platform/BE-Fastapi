import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from numpy import dot
from numpy.linalg import norm

from model.model import RecommenderInput
from utils.cud import create_recommendation 

# 추천 코드 초기화 
def init_recommender():
    global user_embedding
    global contents_embedding_dict
    global best_gbm 
    global contents
    global genres
    global cbf_model_input_scaled
    user_embedding = data_load("resource\mbti_embeddings_dict.pkl")
    contents_embedding_dict = data_load("resource\contents_embeddings_dict.pkl")
    best_gbm = joblib.load('resource\gbm_model.pkl')
    data = pd.read_csv('resource\media_data.csv', encoding='utf-8')
    contents = data[['Title', 'Genres', 'Overview', 'Rating Value', 'Rating Count']]
    contents = normalize_popularity_score(contents)

    # 영화 장르 원핫 인코딩
    genres = contents['Genres'].str.get_dummies(sep=', ')

    cbf_model_input = np.hstack([genres.values, contents['Rating Value'].values.reshape(-1, 1)])
    cbf_scaler = StandardScaler()
    cbf_model_input_scaled = cbf_scaler.fit_transform(cbf_model_input)

# 피클 데이터 불러오기 
def data_load(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def normalize_popularity_score(content):
    scaler = MinMaxScaler()
    content['Normalized Popularity Score'] = scaler.fit_transform(content[['Rating Count']])
    return content

# 영화와 MBTI 유형 간의 유사도 계산 함수
async def calculate_similarity(embedding, user_embedding):
    return dot(embedding, user_embedding) / (norm(embedding) * norm(user_embedding))

# 1. MBTI 임베딩 기반 추천
async def recommend_contents_by_mbti(user_embedding, top_n=100):
    recommended_contents = []
    for content, embedding in contents_embedding_dict.items():
        similarity = await calculate_similarity(embedding, user_embedding)
        recommended_contents.append((content, similarity))
    recommended_contents = sorted(recommended_contents, key=lambda x: x[1], reverse=True)
    return recommended_contents[:top_n]

# 2. 선호 영화 유사도 기반 추천
async def recommend_similar_contents(preferred_contents, top_n=100):
    similar_contents = {}
    for contents in preferred_contents:
        contents_embedding = contents_embedding_dict[contents]
        for other_content, embedding in contents_embedding_dict.items():
            if other_content not in preferred_contents:
                similarity = await calculate_similarity(embedding, contents_embedding)
                if other_content not in similar_contents:
                    similar_contents[other_content] = 0
                similar_contents[other_content] += similarity
    similar_contents = sorted(similar_contents.items(), key=lambda x: x[1], reverse=True)
    return similar_contents[:top_n]

async def calculate_score(recommendations, weight ,combined_recommendations):
    # MBTI 유사도 점수 보정
    scores = [score for _, score in recommendations]
    std = np.std(scores)
    scores_normalized = [score / std for score in scores]

    for (content_id, _), score in zip(recommendations, scores_normalized):
        if content_id not in combined_recommendations:
            combined_recommendations[content_id] = 0
        combined_recommendations[content_id] += weight * score
    return combined_recommendations

async def get_recommendations(ri:RecommenderInput,db,weight_mbti=0.3, weight_similar=0.4, weight_model=0.1, weight_popularity = 0.2, top_n=20):
    new_user_embedding = user_embedding[ri.mbti]
    
    if ri.previous_recommendations:
        exclude_contents = set(ri.previous_recommendations).union(set(ri.preference))
        re_recommendation = True
    else:
        exclude_contents = set()
        re_recommendation = False

    mbti_recommendations = await recommend_contents_by_mbti(new_user_embedding, top_n=100)
    similar_contents_recommendations = await recommend_similar_contents(ri.preference, top_n=100)
    combined_recommendations = {}
    combined_recommendations = await calculate_score(mbti_recommendations, weight_mbti, combined_recommendations)
    combined_recommendations = await calculate_score(similar_contents_recommendations, weight_similar, combined_recommendations)

 # 모델 점수 보정
    content_indices = [contents.index[contents['Title'] == content_id][0] for content_id in combined_recommendations.keys() ]

    if content_indices:
        content_features = cbf_model_input_scaled[content_indices]
        model_scores = best_gbm.predict(content_features).flatten()
        model_std = np.std(model_scores)
        model_scores_normalized = [score / model_std for score in model_scores]

        for content_id, model_score in zip(combined_recommendations.keys(), model_scores_normalized):
            combined_recommendations[content_id] += weight_model * model_score
    
        # 대중성 점수 보정
    popularity_scores = [contents.loc[contents['Title'] == content_id, 'Normalized Popularity Score'].values[0] for content_id in combined_recommendations.keys()]
    popularity_std = np.std(popularity_scores)
    popularity_scores_normalized = [score / popularity_std for score in popularity_scores]

    for content_id, popularity_score in zip(combined_recommendations.keys(), popularity_scores_normalized):
        combined_recommendations[content_id] += weight_popularity * popularity_score

    filtered_recommendations = {content: score for content, score in combined_recommendations.items()
                                if content not in exclude_contents and contents.loc[contents['Title'] == content, 'Rating Value'].values[0] >= 3.5}

    final_recommendations = sorted(filtered_recommendations.items(), key=lambda x: x[1], reverse=True)
    result = [content for content, _ in final_recommendations[:top_n]]
    await create_recommendation(ri, result, re_recommendation, db)
    return result
