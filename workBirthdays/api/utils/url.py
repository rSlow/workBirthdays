from pydantic import AnyHttpUrl


def url_to_str(url: AnyHttpUrl | None) -> str | None:
    if url is not None:
        return url.unicode_string()
