from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.login_page import LoginPage


class HomePage(BasePage):
    def is_authenticated(self) -> bool:
        # Đổi URL đơn thuần chưa chứng minh đăng nhập thành công.
        return (
            self.is_same_origin()
            and not LoginPage(self.driver, self.settings).is_loaded()
            and self.any_visible((By.CSS_SELECTOR, self.settings.authenticated_css))
        )

    def wait_until_authenticated(self):
        self.wait.until(
            lambda driver: self.is_authenticated(),
            "Không thấy trang đã xác thực; kiểm tra tài khoản và UTC_AUTHENTICATED_CSS.",
        )
        return self

    def open_protected(self):
        self.driver.get(self.settings.protected_url)
        return self

    def logout(self):
        self.click((By.CSS_SELECTOR, self.settings.logout_css))
        return LoginPage(self.driver, self.settings).wait_until_loaded()
