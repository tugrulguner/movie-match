import pandas as pd
import pickle
import os
import requests
from dotenv import load_dotenv
from rest_framework import viewsets
from django.http import JsonResponse
from sentence_transformers import (
    SentenceTransformer, 
    util
)

load_dotenv()

class MovieMatch(viewsets.GenericViewSet):
    
    def __init__(self, *args, **kwargs):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.data = pd.read_csv('rottentomatoes-400k.csv')
        self.embedding_1 = pickle.load(open('verse-embeddings_full.pkl', 'rb'))

    def create(self, request) -> JsonResponse:
        input_embedding = self.model.encode(
            request.data['user_input'], 
            convert_to_tensor=True
        )
        result = util.semantic_search(
            input_embedding, 
            self.embedding_1, 
            top_k=request.data['top_k']
        )
        filtered_result = {
            element['corpus_id']: self.data['Movie'].loc[element['corpus_id']] 
            for element in result[0]
        }
        return JsonResponse(filtered_result)
   
class TMDBResult(viewsets.GenericViewSet) :
    
    def __init__(self, *args, **kwargs):
        pass

    def create(self, request) -> JsonResponse:
        ai_return = requests.post(
            'http://127.0.0.1:8000/movie-match/', 
            json={
                'user_input': request.data['user_input'],
                'top_k': request.data['top_k']
            }
        )
        tmdb_return_dict = {}
        for _, movie_name in ai_return.json().items():
            tmdb_return = requests.get(
                f'https://api.themoviedb.org/3/search/movie?query={movie_name}',
                headers = {
                    'accept': 'application/json',
                    'Authorization': f'Bearer {os.getenv("tmdb_token")}'
                }
            )
            tmdb_return_dict[movie_name] = [
                element for element in tmdb_return.json()['results'] 
                    if movie_name.lower()==element['original_title'].lower() 
            ]
            
        return JsonResponse(tmdb_return_dict)