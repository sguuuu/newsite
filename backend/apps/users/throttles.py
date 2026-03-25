from rest_framework.throttling import AnonRateThrottle


class RegistrationThrottle(AnonRateThrottle):
    """Не более 5 регистраций с одного IP в час."""
    scope = 'registration'


class LoginThrottle(AnonRateThrottle):
    """Не более 10 попыток входа с одного IP в час."""
    scope = 'login'


class PasswordResetThrottle(AnonRateThrottle):
    """Не более 3 запросов сброса пароля с одного IP в час."""
    scope = 'password_reset'
