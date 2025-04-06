class DomainException(Exception):
    """Base exception for domain layer"""
    pass

class RouteNotFoundError(DomainException):
    """Raised when route cannot be found"""
    def __init__(self, route_id: str):
        super().__init__(f"Route with ID {route_id} not found")
        self.route_id = route_id

class InvalidRouteError(DomainException):
    """Raised when route data is invalid"""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.errors = errors or {}

class TrafficAlertConflictError(DomainException):
    """Raised when traffic alert conflicts with existing one"""
    def __init__(self, existing_alert_id: str, new_alert_id: str):
        super().__init__(
            f"Alert {new_alert_id} conflicts with existing alert {existing_alert_id}"
        )
        self.existing_alert_id = existing_alert_id
        self.new_alert_id = new_alert_id

class TransportUnavailableError(DomainException):
    """Raised when requested transport is not available"""
    def __init__(self, transport_type: str, location: tuple):
        super().__init__(
            f"No available {transport_type} vehicles near {location}"
        )
        self.transport_type = transport_type
        self.location = location

class RouteOptimizationError(DomainException):
    """Raised when route optimization fails"""
    pass