# modules/made_in_leylek/presentation/views/auction_views.py
from fastapi import APIRouter, Depends, HTTPException
from ...application.dto.product_dto import AuctionLotDTO, BidDTO
from ...application.use_cases.auction_management import AuctionUseCase
from ..serializers import (
    AuctionLotResponseSerializer,
    BidResponseSerializer
)
from core.authentication import get_current_user

router = APIRouter(prefix="/auctions", tags=["Auctions"])

@router.post("/", response_model=AuctionLotResponseSerializer)
async def create_auction(
    auction_data: AuctionLotDTO,
    use_case: AuctionUseCase = Depends(AuctionUseCase),
    user: dict = Depends(get_current_user)
):
    """Создание нового аукциона"""
    if not user.get("is_seller"):
        raise HTTPException(status_code=403, detail="Only sellers can create auctions")
    
    try:
        auction = await use_case.create_auction(
            user_id=user["id"],
            auction_data=auction_data
        )
        return AuctionLotResponseSerializer(**auction.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{auction_id}/bids", response_model=BidResponseSerializer)
async def place_bid(
    auction_id: str,
    bid_data: BidDTO,
    use_case: AuctionUseCase = Depends(AuctionUseCase),
    user: dict = Depends(get_current_user)
):
    """Размещение ставки в аукционе"""
    try:
        bid = await use_case.place_bid(
            user_id=user["id"],
            auction_id=auction_id,
            amount=bid_data.amount
        )
        return BidResponseSerializer(**bid.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))