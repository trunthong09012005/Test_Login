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

def test_tc02_empty_password(login):
    login.fill("sample-user", "").submit()
    assert login.error_text() == "Bạn chưa nhập mật khẩu"

@pytest.mark.credentials
def test_tc03_valid_username_wrong_password(login, settings):
    login.fill(settings.username, "utc@235").submit()
    assert_authentication_rejected(login)

@pytest.mark.credentials
def test_tc04_wrong_username_valid_password(login, settings):
    login.fill(f"invalid-{uuid.uuid4()}", settings.password).submit()
    assert_authentication_rejected(login)

@pytest.mark.credentials
@pytest.mark.session
def test_tc05_remember_me_persists_after_browser_restart(login, browser, settings):
    login.login(settings.username, settings.password, remember=True)
    assert not login.is_loaded()
    browser.restart()
    browser.driver.get(settings.protected_url)
    assert not LoginPage(browser.driver, settings).is_loaded()

@pytest.mark.credentials
@pytest.mark.session
def test_tc06_without_remember_me_requires_login_after_restart(login, browser, settings):
    login.login(settings.username, settings.password, remember=False)
    assert not login.is_loaded()
    browser.restart()
    browser.driver.get(settings.protected_url)
    assert LoginPage(browser.driver, settings).is_loaded()

def test_tc07_empty_username_and_password(login):
    login.fill("", "").submit()
    assert "chưa nhập" in login.error_text().lower()

