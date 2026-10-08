import tempfile
from pathlib import Path

from selenium import webdriver

from config import Settings


class BrowserSession:
    """Profile riêng cho từng test, giữ lại profile khi restart TC5/TC6."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.driver = None
        self._profile = tempfile.TemporaryDirectory(prefix="utc-selenium-", ignore_cleanup_errors=True)

    def start(self):
        options = webdriver.ChromeOptions() if self.settings.browser == "chrome" else webdriver.EdgeOptions()
        if self.settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument(f"--user-data-dir={Path(self._profile.name).resolve()}")
        options.add_argument("--no-first-run")
        options.set_capability("unhandledPromptBehavior", "ignore")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        })
        constructor = webdriver.Chrome if self.settings.browser == "chrome" else webdriver.Edge
        self.driver = constructor(options=options)
        self.driver.set_page_load_timeout(45)
        self.driver.set_script_timeout(self.settings.timeout)
        return self.driver

    def restart(self):
        self._quit()
        # Không xóa cookies, không tạo profile khác và không tự khôi phục cookie.
        return self.start()

    def _quit(self):
        if self.driver is not None:
            try:
                self.driver.quit()
            finally:
                self.driver = None

    def close(self):
        try:
            self._quit()
        finally:
            self._profile.cleanup()
