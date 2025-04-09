from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from core.api import JWTAuthentication, handle_exceptions
from ..serializers import (
    SubscriptionSerializer,
    SubscriptionResponseSerializer
)
from modules.hot_news.application.use_cases import SubscriptionManagementUseCase

class SubscriptionAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=SubscriptionSerializer,
        responses={200: SubscriptionResponseSerializer}
    )
    @handle_exceptions
    def get(self, request):
        """Получение текущей подписки пользователя"""
        use_case = SubscriptionManagementUseCase()
        subscription = use_case.get_user_subscription(request.user.id)
        return Response(
            SubscriptionResponseSerializer(subscription).data
        )

    @extend_schema(
        request=SubscriptionSerializer,
        responses={201: SubscriptionResponseSerializer}
    )
    @handle_exceptions
    def post(self, request):
        """Создание или обновление подписки"""
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = SubscriptionManagementUseCase()
        result = use_case.update_subscription(
            request.user.id,
            serializer.to_dto()
        )
        
        return Response(
            SubscriptionResponseSerializer(result).data,
            status=status.HTTP_201_CREATED
        )