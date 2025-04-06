class RouteNotFoundError(Exception):
    """Маршрут не найден"""
    pass

class InvalidCoordinatesError(Exception):
    """Некорректные координаты"""
    pass

class TrafficDataUnavailableError(Exception):
    """Данные о трафике недоступны"""
    pass