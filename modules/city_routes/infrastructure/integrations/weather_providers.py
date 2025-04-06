# infrastructure/integrations/weather_providers.py
class OpenWeatherMapAdapter:
    async def get_route_weather(self, route_id: str, step_km: int):
        # Реализация запросов к API погоды
        pass