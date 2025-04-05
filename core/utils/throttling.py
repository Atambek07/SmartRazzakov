from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


class MunicipalThrottle(UserRateThrottle):
    scope = 'municipal'

    def allow_request(self, request, view):
        if request.user.groups.filter(name='municipal_workers').exists():
            return True
        return super().allow_request(request, view)