import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.home_page import HomePage

AUTHENTICATION_ERROR = "không đúng"

def assert_authentication_rejected(page: LoginPage):
    assert page.is_loaded()
    assert AUTHENTICATION_ERROR.lower() in page.error_text().lower()

def assert_handled_without_server_error(page: LoginPage, driver, settings):
    assert page.is_same_origin()
    usable_result = page.is_loaded() or HomePage(driver, settings).is_authenticated()
    assert usable_result

def test_tc01_empty_username(login):
    login.fill("", "1256").submit()
    assert login.error_text() == "Bạn chưa nhập tên đăng nhập"

