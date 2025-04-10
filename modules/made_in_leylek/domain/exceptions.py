class DomainException(Exception):
    """Базовое исключение для доменных ошибок"""
    pass

class ProductNotFoundError(DomainException):
    """Товар не найден"""
    pass

class InsufficientStockError(DomainException):
    """Недостаточно товара на складе"""
    pass

class AuctionClosedError(DomainException):
    """Аукцион закрыт или завершен"""
    pass

class InvalidBidError(DomainException):
    """Некорректная ставка в аукционе"""
    pass

class GroupPurchaseExpiredError(DomainException):
    """Групповая покупка завершена по времени"""
    pass

class OrderValidationError(DomainException):
    """Ошибка валидации заказа"""
    pass