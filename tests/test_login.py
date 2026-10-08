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

def test_tc08_wrong_username_and_password(login):
    login.fill("abcxyz", "abc123").submit()
    assert_authentication_rejected(login)

@pytest.mark.credentials
def test_tc09_leading_whitespace_in_username(login, settings, browser):
    login.fill(f" {settings.username}", settings.password).submit()
    assert_handled_without_server_error(login, browser.driver, settings)

@pytest.mark.credentials
def test_tc10_trailing_whitespace_in_username(login, settings, browser):
    login.fill(f"{settings.username} ", settings.password).submit()
    assert_handled_without_server_error(login, browser.driver, settings)

@pytest.mark.credentials
def test_tc11_leading_whitespace_in_password(login, settings):
    login.fill(settings.username, f" {settings.password}").submit()
    assert_authentication_rejected(login)

@pytest.mark.credentials
def test_tc12_trailing_whitespace_in_password(login, settings):
    login.fill(settings.username, f"{settings.password} ").submit()
    assert_authentication_rejected(login)

@pytest.mark.credentials
def test_tc13_uppercase_username(login, settings, browser):
    login.fill(settings.username.upper(), settings.password).submit()
    assert_handled_without_server_error(login, browser.driver, settings)

@pytest.mark.credentials
def test_tc14_wrong_password_case(login, settings):
    original_password = settings.password
    changed_case = original_password.upper()
    if changed_case == original_password:
        pytest.skip("Mật khẩu không có chữ để đổi hoa/thường")
    login.fill(settings.username, changed_case).submit()
    assert_authentication_rejected(login)

def test_tc15_special_characters_in_username(login):
    login.fill("@#$%^&*", "arbitrary-password").submit()
    assert_authentication_rejected(login)

def test_tc16_special_characters_in_password(login):
    login.fill("sample-user", "!@#$%^&*").submit()
    assert_authentication_rejected(login)

def test_tc17_username_at_excessive_length(login, browser, settings):
    long_username = "u" * 256
    login.fill(long_username, "arbitrary-password")
    accepted_length = login.username_length()
    login.submit()
    assert accepted_length <= 256
    assert_handled_without_server_error(login, browser.driver, settings)

def test_tc18_password_at_excessive_length(login, browser, settings):
    long_password = "p" * 256
    login.fill("sample-user", long_password)
    accepted_length = login.password_length()
    login.submit()
    assert accepted_length <= 256
    assert_handled_without_server_error(login, browser.driver, settings)

def test_tc19_password_is_masked(login):
    login.fill("", "123456@utc")
    assert login.password_type() == "password"

@pytest.mark.credentials
def test_tc20_submit_login_with_enter(login, settings):
    login.login(settings.username, settings.password, enter=True)
    assert not login.is_loaded()

@pytest.mark.credentials
@pytest.mark.rate_limit
def test_tc21_five_consecutive_failed_logins(login, settings):
    for attempt in range(1, 6):
        login.fill(settings.username, f"wrong-password-{attempt}").submit()
        assert_authentication_rejected(login)

@pytest.mark.credentials
@pytest.mark.session
def test_tc22_logout_after_successful_login(login, settings, browser):
    home = login.login(settings.username, settings.password)
    assert not login.is_loaded()
    
    assert home.any_visible((By.CSS_SELECTOR, settings.logout_css)), "Trang chủ phải có điều khiển Đăng xuất"
    home.logout()
    assert LoginPage(browser.driver, settings).is_loaded()

def test_tc23_protected_page_redirects_anonymous_user(browser, settings):
    browser.driver.get(settings.protected_url)
    WebDriverWait(browser.driver, 15).until(EC.url_contains("/Login"))
    assert "/Login" in browser.driver.current_url

@pytest.mark.security
def test_tc24_sql_injection_is_rejected(login):
    login.fill("' OR '1'='1", "arbitrary-password").submit()
    assert login.is_loaded()

@pytest.mark.security
def test_tc25_script_injection_is_not_executed(login):
    login.fill("<script>alert(1)</script>", "arbitrary-password").submit()
    assert login.is_loaded()
    assert not login.has_alert()

