from fastapi import APIRouter
from .views.public_api import router as public_router
from .views.admin_api import router as admin_router


from .views.weather_api import router as weather_router
from .views.events_api import router as events_router
from .views.parking_api import router as parking_router

admin_router.include_router(weather_router)
admin_router.include_router(events_router)
admin_router.include_router(parking_router)

# Основной роутер
main_router = APIRouter()

# Включаем подроутеры
main_router.include_router(
    public_router,
    prefix="/public/v1",
    tags=["Public API"]
)

main_router.include_router(
    admin_router,
    prefix="/admin/v1",
    tags=["Admin API"],
    # dependencies=[Depends(validate_admin_token)]
)

# Экспортируем для использования в main.py
def get_app():
    from fastapi import FastAPI
    app = FastAPI(
        title="Smart Razakov API",
        description="Цифровая платформа города Раззаков",
        version="1.0.0",
    )
    app.include_router(main_router)
    return app