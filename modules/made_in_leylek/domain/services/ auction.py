# modules/made_in_leylek/domain/services/auction.py
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict
from ....core.exceptions import (
    ValidationError,
    NotFoundError,
    AuctionClosedError
)
from ....core.logging import logger
from ..entities import AuctionEntity, ProductEntity

class AuctionService:
    def __init__(
        self,
        auction_repository,
        payment_gateway,
        notification_service
    ):
        self.repo = auction_repository
        self.payment = payment_gateway
        self.notifier = notification_service

    async def create_auction(
        self,
        product: ProductEntity,
        start_price: Decimal,
        min_increment: Decimal,
        duration_hours: int
    ) -> AuctionEntity:
        """Создание нового аукциона с валидацией"""
        self._validate_auction_params(product, start_price, min_increment)
        
        auction = AuctionEntity(
            product_id=product.id,
            start_price=start_price,
            current_bid=start_price,
            min_increment=min_increment,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=duration_hours),
            status="active",
            bids=[]
        )
        
        await self.repo.save(auction)
        logger.info(f"Created auction {auction.id} for product {product.id}")
        return auction

    async def place_bid(
        self,
        auction_id: str,
        user_id: str,
        amount: Decimal
    ) -> AuctionEntity:
        """Обработка новой ставки"""
        auction = await self._get_active_auction(auction_id)
        
        if amount < auction.current_bid + auction.min_increment:
            raise ValidationError("Ставка ниже минимально допустимой")
            
        if not await self.payment.reserve_funds(user_id, amount):
            raise ValidationError("Недостаточно средств для ставки")
            
        auction.bids.append({
            "user_id": user_id,
            "amount": amount,
            "timestamp": datetime.now()
        })
        auction.current_bid = amount
        
        updated = await self.repo.update(auction)
        await self._notify_participants(auction)
        
        return updated

    async def close_auction(self, auction_id: str) -> Dict:
        """Завершение аукциона и обработка результатов"""
        auction = await self._get_auction(auction_id)
        
        if datetime.now() < auction.end_time:
            raise ValidationError("Аукцион еще не завершен")
            
        winner = self._determine_winner(auction.bids)
        if not winner:
            logger.info(f"No winner for auction {auction_id}")
            return {"status": "no_winner"}
            
        await self.payment.charge(winner['user_id'], winner['amount'])
        await self.notifier.send(
            user_id=winner['user_id'],
            template="auction_won",
            context={"auction_id": auction_id}
        )
        
        auction.status = "completed"
        await self.repo.update(auction)
        
        return {
            "winner": winner['user_id'],
            "amount": winner['amount'],
            "product_id": auction.product_id
        }

    def _validate_auction_params(
        self,
        product: ProductEntity,
        start_price: Decimal,
        min_increment: Decimal
    ):
        if product.quantity < 1:
            raise ValidationError("Товар отсутствует на складе")
        if start_price <= 0:
            raise ValidationError("Начальная цена должна быть положительной")
        if min_increment <= 0:
            raise ValidationError("Минимальный шаг должен быть положительным")

    async def _get_active_auction(self, auction_id: str) -> AuctionEntity:
        auction = await self.repo.get(auction_id)
        if not auction:
            raise NotFoundError("Аукцион не найден")
        if auction.status != "active":
            raise AuctionClosedError("Аукцион закрыт")
        return auction

    def _determine_winner(self, bids: List[Dict]) -> Optional[Dict]:
        return max(bids, key=lambda x: x['amount'], default=None)

    async def _notify_participants(self, auction: AuctionEntity):
        participants = {bid['user_id'] for bid in auction.bids}
        for user_id in participants:
            await self.notifier.send(
                user_id=user_id,
                template="new_bid",
                context={
                    "auction_id": auction.id,
                    "current_bid": auction.current_bid
                }
            )