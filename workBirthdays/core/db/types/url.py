from pydantic import AnyUrl
from sqlalchemy_utils import URLType


class PydanticURLType(URLType):
    def process_bind_param(self, value, dialect):
        if isinstance(value, AnyUrl):
            return value.unicode_string()
        return super().process_bind_param(value, dialect)
