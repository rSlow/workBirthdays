from typing import Callable

from selenium.webdriver.remote.webelement import WebElement

PartialFind = Callable[[str], WebElement]
