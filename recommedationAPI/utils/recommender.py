import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from numpy import dot
from numpy.linalg import norm

from model.data.model import RecommenderInput

# 영화와 MBTI 유형 간의 유사도 계산 함수
async def calculate_similarity(embedding, user_embedding):
    return dot(embedding, user_embedding) / (norm(embedding) * norm(user_embedding))

# 1. MBTI 임베딩 기반 추천
async def recommend_contents_by_mbti(user_embedding, top_n=100):
    recommended_contents = []
    for content, embedding in contents_embedding_dict.items():
        similarity = await calculate_similarity(embedding, user_embedding)
        recommended_contents.append((content, similarity))
    recommended_movies = sorted(recommended_contents, key=lambda x: x[1], reverse=True)
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
    for content, score in recommendations:
        if content not in combined_recommendations:
            combined_recommendations[content] = 0
        combined_recommendations[content] += weight * score
    return combined_recommendations

# 결합 추천 시스템
async def recommend_contents_combined(user_embedding, preferred_contents,
                              weight_mbti=0.4, weight_similar=0.5, weight_model=0.1, top_n=20):
    mbti_recommendations = await recommend_contents_by_mbti(user_embedding, top_n=100)
    similar_contents_recommendations = await recommend_similar_contents(preferred_contents, top_n=100)

    combined_recommendations = {}

    combined_recommendations = await calculate_score(mbti_recommendations, weight_mbti, combined_recommendations)
    combined_recommendations = await calculate_score(similar_contents_recommendations, weight_similar, combined_recommendations)

    content_indices = [contents[contents['index'] == content].index[0] for content in combined_recommendations.keys()]
    if content_indices:
        content_features = cbf_model_input_scaled[content_indices]
        model_scores = best_gbm.predict(content_features).flatten()

        for content, model_score in zip(combined_recommendations.keys(), model_scores):
            combined_recommendations[content] += weight_model * model_score

    filtered_recommendations = {content: score for content, score in combined_recommendations.items()
                                if contents.loc[contents['name'] == content, 'star_avg'].values[0] >= 3.0}

    final_recommendations = sorted(filtered_recommendations.items(), key=lambda x: x[1], reverse=True)
    return [content for content, _ in final_recommendations[:top_n]]


async def recommendation(ri:RecommenderInput):
    new_user_embedding = user_embedding[ri.mbti]
    result = await recommend_contents_combined(new_user_embedding, ri.preference)
    return result

def init_recommneder():
    global user_embedding
    global contents_embedding_dict
    global best_gbm 
    global contents
    global genres
    global cbf_model_input_scaled
    user_embedding = data_load("resource\mbti_embeddings_dict.pkl")
    contents_embedding_dict = data_load("resource\contents_embeddings_dict.pkl")
    best_gbm = joblib.load('resource/gbm_model.pkl')
    contents = pd.read_csv('resource\contents_meta_data_final.csv', encoding='utf-8')
    
    # 영화 장르 원핫 인코딩
    genres = contents['genres'].str.get_dummies(sep=',')

    cbf_model_input = np.hstack([genres.values, contents['star_avg'].values.reshape(-1, 1)])
    cbf_scaler = StandardScaler()
    cbf_model_input_scaled = cbf_scaler.fit_transform(cbf_model_input)
    
def data_load(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)