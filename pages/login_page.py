from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Xác nhận từ HTML công khai của trang UTC và slide Buổi 8.
    _USERNAME = (By.NAME, "username")
    _PASSWORD = (By.NAME, "userpwd")
    _REMEMBER = (By.ID, "persistent")
    _REMEMBER_LABEL = (By.CSS_SELECTOR, "label.check[for='persistent']")
    _SUBMIT = (By.CSS_SELECTOR, "input.submit_login")
    _FORM = (By.CSS_SELECTOR, "form[action='/Login']")
    _ERROR = (By.CSS_SELECTOR, "form .error")

    def open(self):
        self.driver.get(self.settings.login_url)
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        self.visible(self._USERNAME)
        self.visible(self._PASSWORD)
        self.visible(self._SUBMIT)
        return self

    def is_loaded(self) -> bool:
        return self.is_same_origin() and self.any_visible(self._FORM)

    def fill(self, username: str, password: str):
        self.type_text(self._USERNAME, username)
        self.type_text(self._PASSWORD, password)
        return self

    def remember_me(self, enabled: bool):
        checkbox = self.wait.until(EC.presence_of_element_located(self._REMEMBER))
        if checkbox.is_selected() != enabled:
            self.click(self._REMEMBER_LABEL)
        self.wait.until(EC.element_located_selection_state_to_be(self._REMEMBER, enabled))
        return self

    def remember_is_checked(self) -> bool:
        return self.driver.find_element(*self._REMEMBER).is_selected()

    def submit(self, *, enter: bool = False):
        # Trang UTC POST form và tải document mới. Chờ form CŨ biến mất,
        # tránh đọc lại lỗi của lần submit trước (đặc biệt TC21).
        old_form = self.visible(self._FORM)
        if enter:
            self.visible(self._PASSWORD).send_keys(Keys.ENTER)
        else:
            self.click(self._SUBMIT)
        self.wait.until(EC.staleness_of(old_form))
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        return self

    def login(self, username: str, password: str, *, remember: bool = False, enter: bool = False):
        from pages.home_page import HomePage

        self.fill(username, password).remember_me(remember).submit(enter=enter)
        return HomePage(self.driver, self.settings)

    def error_text(self) -> str:
        return self.visible(self._ERROR).text.strip()

    def password_type(self) -> str:
        return self.visible(self._PASSWORD).get_dom_attribute("type")

    def password_length(self) -> int:
        return len(self.visible(self._PASSWORD).get_property("value"))

    def username_length(self) -> int:
        return len(self.visible(self._USERNAME).get_property("value"))

    def input_max_length(self, field: str) -> int | None:
        locator = {"username": self._USERNAME, "password": self._PASSWORD}[field]
        value = self.visible(locator).get_dom_attribute("maxlength")
        return int(value) if value and value.isdigit() else None

    def has_alert(self) -> bool:
        return bool(EC.alert_is_present()(self.driver))
