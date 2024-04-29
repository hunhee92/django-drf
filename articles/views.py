from django.shortcuts import get_object_or_404, render
from .models import Article, Comment
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer
from drf_spectacular.utils import extend_schema
# Create your views here.


# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         # json_data = serializer
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):  # raise가 밑에 return 기능 대신해줌
#             serializer.save()
#             # from rest_framework import status
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=400)


# @api_view(['GET', 'PUT', 'DELETE'])
# def article_detail(request, pk):
#     if request.method == 'GET':
#         articles = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(articles)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         articles = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(
#             articles, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == 'DELETE':
#         articles = get_object_or_404(Article, pk=pk)
#         articles.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Articles'],
        description="Aticle 목록을 위한 API",
        request=ArticleDetailSerializer
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # json_data = serializer
        return Response(serializer.data)

    @extend_schema(
        tags=['Articles'],
        description="Aticle 생성을 위한 API",
        request=ArticleDetailSerializer
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # raise가 밑에 return 기능 대신해줌
            serializer.save()
            # from rest_framework import status
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        articles = self.get_object(pk)
        serializer = ArticleDetailSerializer(articles)
        return Response(serializer.data)

    def put(self, request, pk):
        articles = self.get_object(pk)
        serializer = ArticleDetailSerializer(
            articles, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        articles = self.get_object(pk)
        articles.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def check_sql(request):
    from django.db import connection

    # sql 쿼리를 볼수있는 connection 임포트
    comments = Comment.objects.all().select_related("article")
    # 정방향 참조일땐 select_related사용, 아래에서 필요한 데이터를 한번에 가져옴
    for comment in comments:
        print(comment.article.title)
        # 위에서 한번에 데이터를 가져 왔기에 가져온 데이터로 출력만함
        # select_related를 사용안했을 땐 n번의 쿼리문이 발생

    print("-" * 40)
    print(connection.queries)

    return Response(status=status.HTTP_200_OK)

# @api_view(['GET'])
# def check_sql(request):
#     from django.db import connection

#     # sql 쿼리를 볼수있는 connection 임포트
#     articles = Article.object.all().prefetch_related("comments")
#     # 역방향 참조 (모델에서 포린키는 Comment에 있음,정참조에도 쓸 수 있다) 아티클 정보조회하고 코멘트까지 가져와라
#     for article in articles:
#         comments = article.comments.all()
#         # 위에서 한번에 데이터를 가져 왔기에 가져온 데이터로 출력만함
#         # prefetch_related를 사용안했을 땐 n번의 쿼리문이 발생
    # for comment in comments:
    #   print(comment.content)

#     print("-" * 40)
#     print(connection.queries)

#     return Response(status=status.HTTP_200_OK)
