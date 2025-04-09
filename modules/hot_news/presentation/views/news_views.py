from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from core.api import (
    JWTAuthentication,
    AdminPermission,
    EditorPermission,
    handle_exceptions
)
from ..serializers import (
    NewsCreateSerializer,
    NewsUpdateSerializer,
    NewsResponseSerializer
)
from modules.hot_news.application.use_cases import NewsManagementUseCase

class NewsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [EditorPermission]

    @extend_schema(
        request=NewsCreateSerializer,
        responses={201: NewsResponseSerializer}
    )
    @handle_exceptions
    def post(self, request):
        """Создание новостной статьи"""
        serializer = NewsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = NewsManagementUseCase()
        result = use_case.create_article(
            serializer.to_dto(),
            request.user.id
        )
        
        return Response(
            NewsResponseSerializer(result).data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='category', type=str),
            OpenApiParameter(name='priority', type=int)
        ],
        responses={200: NewsResponseSerializer(many=True)}
    )
    @handle_exceptions
    def get(self, request):
        """Получение списка новостей с фильтрацией"""
        use_case = NewsManagementUseCase()
        articles = use_case.list_articles(
            category=request.query_params.get('category'),
            priority=request.query_params.get('priority')
        )
        serializer = NewsResponseSerializer(articles, many=True)
        return Response(serializer.data)

class NewsDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [EditorPermission]

    @extend_schema(responses={200: NewsResponseSerializer})
    @handle_exceptions
    def get(self, request, article_id):
        """Получение деталей новости"""
        use_case = NewsManagementUseCase()
        article = use_case.get_article(article_id)
        return Response(NewsResponseSerializer(article).data)

    @extend_schema(
        request=NewsUpdateSerializer,
        responses={200: NewsResponseSerializer}
    )
    @handle_exceptions
    def put(self, request, article_id):
        """Обновление новости"""
        serializer = NewsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = NewsManagementUseCase()
        result = use_case.update_article(
            article_id,
            serializer.to_dto()
        )
        
        return Response(NewsResponseSerializer(result).data)

    @extend_schema(responses={204: None})
    @handle_exceptions
    def delete(self, request, article_id):
        """Удаление новости"""
        use_case = NewsManagementUseCase()
        use_case.delete_article(article_id)
        return Response(status=status.HTTP_204_NO_CONTENT)