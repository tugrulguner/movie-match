import pandas as pd
import pickle

from rest_framework import viewsets
from django.http import JsonResponse, StreamingHttpResponse
from sentence_transformers import (
    SentenceTransformer, 
    util
)

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