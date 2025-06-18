from .config import ApiProvider
from .auth import AuthProvider


def get_api_providers():
    return [
        ApiProvider(),
        AuthProvider()
    ]
