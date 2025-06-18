from workBirthdays.core.utils.exceptions import BaseError


class AuthError(BaseError):
    log = False


class EmptyPayloadError(AuthError):
    user_note_template = "Empty payload in valid JWT token"


class InvalidJWTError(AuthError):
    user_note_template = "JWT is invalid"


class AuthHeaderMissingError(AuthError):
    user_note_template = "Header not contain authentication token"


class UnknownSchemaError(AuthError):
    user_note_template = "Unknown authentication schema: {schema}"
