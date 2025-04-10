# modules/made_in_leylek/presentation/urls.py
from fastapi import APIRouter
from .views.auction_views import auction_router
from .views.buyer_views import buyer_router
from .views.seller_views import seller_router

router = APIRouter()

router.include_router(
    auction_router,
    prefix="/api/v1",
    tags=["Auctions"]
)

router.include_router(
    buyer_router,
    prefix="/api/v1",
    tags=["Buyer"]
)

router.include_router(
    seller_router,
    prefix="/api/v1",
    tags=["Seller"]
)

# Health check endpoint
@router.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}