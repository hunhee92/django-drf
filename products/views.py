from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.core.cache import cache
# Create your views here.


class ProductsListAPIView(APIView):
    def get(self, request):
        cache_key = "product_list"
        # 캐시는 키와 밸류의 형태 캐시 이름을 선언
        if not cache.get(cache_key):  # cache.get(key)캐시 데이터를 불러오는 방법  if 문에선 데이터가 없을때
            # db에서 데이터를 전부 불러와서 저장
            print("cache miss")
            products = Product.objects.all()
            # db에 있는 Product를 전부 가져지고 옴
            serializers = ProductSerializer(products, many=True)
            # 가져온 데이터를 직렬화 many 옵션은 데이터가 많을때 True
            json_data = serializers.data
            # 직렬화 한 데이터를 볼때 .data 사용
            cache.set(cache_key, json_data)
            # db 에서 가지고온 데이터를 캐시에 저장 // cache.set 은 생성 명령어 (키이름 ,밸류 , 유효시간)

        json_data = cache.get(cache_key)  # 만약 캐시에 데이터가 있으면 get 으로 가져와서
        return Response(json_data)  # 전 송 ~ !
