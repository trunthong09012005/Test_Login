from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import Settings


class BasePage:
    def __init__(self, driver, settings: Settings):
        self.driver = driver
        self.settings = settings
        self.wait = WebDriverWait(driver, settings.timeout)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        element = self.visible(locator)
        element.clear()
        if text:
            element.send_keys(text)

    def any_visible(self, locator) -> bool:
        try:
            return any(element.is_displayed() for element in self.driver.find_elements(*locator))
        except StaleElementReferenceException:
            return False

    def is_same_origin(self) -> bool:
        expected = urlparse(self.settings.login_url)
        actual = urlparse(self.driver.current_url)
        return (actual.scheme, actual.netloc) == (expected.scheme, expected.netloc)

    def visible_server_errors(self) -> list[str]:
        """Chỉ kiểm tra dấu hiệu lỗi lộ trên UI, không thay thế security audit."""
        body = self.visible((By.TAG_NAME, "body")).text.lower()
        indicators = (
            "internal server error", "stack trace", "sqlstate[", "sql syntax",
            "database error", "fatal error", "uncaught exception", "traceback (most recent call last)",
        )
        return [text for text in indicators if text in body]
