import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from concurrent.futures import ThreadPoolExecutor
from tensorflow import keras
import pickle
from typing import List
from model.model import content


# 임베딩을 생성하는 함수
async def sentence_embedding(sentence):
  return labse_model(tf.constant([sentence]))[0].numpy().astype(np.float64)

# 병렬 처리를 이용하여 임베딩 생성
async def parallel_embedding(texts):
    with ThreadPoolExecutor() as executor:
        embeddings = list(executor.map(sentence_embedding, texts))
    return np.array(embeddings).astype(np.float64)

# content DB가 변경된 경우 embedding 생성 
async def content_embedding(contents: List[content]):
  # 한국어 영화 줄거리 임베딩 병렬 처리
  contents_texts = contents['overview'].tolist()
  contents_embeddings = await parallel_embedding(contents_texts)
  contents_index = contents['index'].tolist()
  contents_embeddings_dict = dict(zip(contents_index, contents_embeddings))

  with open('resource/contents_embeddings_dict.pkl', 'wb') as f:
    pickle.dump(contents_embeddings_dict, f)
  

# def init_embedding():
#   global labse_model
#   global contents 
#   model_path = 'resource/labse_model.h5'
#   labse_model = keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})
#   contents = pd.read_csv('resource\contents_meta_data_final.csv', encoding='utf-8')
    
# def data_load(file_path):
#   with open(file_path, 'rb') as f:
#       return pickle.load(f)