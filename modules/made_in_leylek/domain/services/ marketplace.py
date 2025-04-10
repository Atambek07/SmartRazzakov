# modules/made_in_leylek/domain/services/marketplace.py
from decimal import Decimal
from typing import List, Dict, Optional
from ....core.exceptions import (
    ProductNotFoundError,
    InvalidSearchQuery,
    RecommendationError
)
from ....core.logging import logger
from ..entities import ProductEntity, OrderEntity

class MarketplaceService:
    def __init__(
        self,
        product_repository,
        order_repository,
        search_engine,
        recommendation_engine
    ):
        self.products = product_repository
        self.orders = order_repository
        self.search = search_engine
        self.recommendations = recommendation_engine

    async def search_products(
        self,
        query: str,
        filters: Optional[Dict] = None,
        sort_by: str = "relevance"
    ) -> List[ProductEntity]:
        """Поиск товаров с фильтрацией и сортировкой"""
        try:
            search_results = await self.search.execute(
                query=query,
                filters=self._normalize_filters(filters),
                sort=sort_by
            )
            return await self.products.bulk_load(search_results['ids'])
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise InvalidSearchQuery("Ошибка поискового запроса")

    async def get_recommendations(
        self,
        user_id: Optional[str] = None,
        product_id: Optional[str] = None
    ) -> List[ProductEntity]:
        """Получение персонализированных рекомендаций"""
        try:
            if user_id:
                user_history = await self.orders.get_user_history(user_id)
                return await self.recommendations.for_user(user_history)
                
            if product_id:
                return await self.recommendations.for_product(product_id)
                
            return await self.recommendations.top_products()
        except Exception as e:
            logger.error(f"Recommendation error: {str(e)}")
            raise RecommendationError("Не удалось получить рекомендации")

    async def update_product_rating(
        self,
        product_id: str,
        new_rating: float
    ) -> ProductEntity:
        """Обновление рейтинга продукта с учетом новых отзывов"""
        product = await self.products.get(product_id)
        if not product:
            raise ProductNotFoundError()
            
        # Экспоненциальное сглаживание рейтинга
        updated_rating = (product.rating * 0.8) + (new_rating * 0.2)
        
        return await self.products.update(
            product_id,
            {"rating": round(updated_rating, 1)}
        )

    async def get_sales_analytics(
        self,
        period_days: int = 30,
        category: Optional[str] = None
    ) -> Dict:
        """Аналитика продаж за указанный период"""
        orders = await self.orders.get_by_period(period_days)
        filtered = [
            o for o in orders
            if not category or any(
                item['category'] == category for item in o.items)
        ]
        
        return {
            "total_sales": sum(o.total_amount for o in filtered),
            "order_count": len(filtered),
            "popular_products": self._get_top_products(filtered),
            "category_distribution": self._get_category_distribution(filtered)
        }

    def _normalize_filters(self, filters: Dict) -> Dict:
        return {
            "price_range": (
                filters.get('min_price'),
                filters.get('max_price')
            ),
            "category": filters.get('category'),
            "rating": filters.get('min_rating', 4.0)
        }

    def _get_top_products(self, orders: List[OrderEntity], top_n: int = 5) -> List:
        product_counts = {}
        for order in orders:
            for item in order.items:
                product_counts[item['product_id']] = product_counts.get(item['product_id'], 0) + 1
        return sorted(product_counts.items(), key=lambda x: -x[1])[:top_n]

    def _get_category_distribution(self, orders: List[OrderEntity]) -> Dict:
        categories = {}
        for order in orders:
            for item in order.items:
                categories[item['category']] = categories.get(item['category'], 0) + 1
        return categories