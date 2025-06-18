import logging
import pickle
from pathlib import Path
from typing import TypedDict, Literal
from urllib.parse import urlparse

from selenium.webdriver.remote.webdriver import WebDriver

from workBirthdays.mq.utils.exceptions import PageError

logger = logging.getLogger(__name__)


class Cookie(TypedDict):
    domain: str
    expiry: int
    httpOnly: bool
    name: str
    path: str
    sameSite: Literal["Strict", "Lax", "None"]
    secure: bool
    value: str


class RequestContext:
    def __init__(self, driver: WebDriver, cookie_file: Path):
        self._driver = driver
        self._cookie_file = cookie_file

    def __enter__(self):
        current_url = urlparse(self._driver.current_url)
        try:
            with open(self._cookie_file, "rb") as file:
                cookies: list[Cookie] = pickle.load(file)
                for cookie in cookies:
                    if cookie["domain"].startswith("."):
                        domain = cookie["domain"][1:]
                    else:
                        domain = cookie["domain"]
                    if current_url.netloc.endswith(domain):
                        try:
                            self._driver.add_cookie(cookie)
                        except Exception as ex:
                            logger.warning(
                                "error on load cookies: " + repr(ex) + f": {cookie.get('name')}"
                            )
        except FileNotFoundError:
            pass

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, PageError):
            return
        cookies: list[Cookie] = self._driver.get_cookies()
        if cookies:
            with open(self._cookie_file, "wb") as file:
                pickle.dump(cookies, file)
