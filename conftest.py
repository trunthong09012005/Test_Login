import hashlib
import re
from dataclasses import replace
from pathlib import Path

import pytest
import pytest_html

from config import Settings
from pages.login_page import LoginPage
from utils.browser import BrowserSession


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "edge"], default=None)
    parser.addoption("--headed", action="store_true", help="Hiện cửa sổ trình duyệt")
    parser.addoption("--run-sensitive", action="store_true", help="Chạy thêm TC21, TC24, TC25")


@pytest.fixture(scope="session")
def settings(pytestconfig):
    config = Settings.from_env()
    return replace(
        config,
        browser=pytestconfig.getoption("--browser") or config.browser,
        headless=False if pytestconfig.getoption("--headed") else config.headless,
    )


@pytest.fixture(autouse=True)
def case_requirements(request, settings):
    """Skip lý do rõ ràng TRƯỚC khi mở browser; skip không có nghĩa là pass."""
    if request.node.get_closest_marker("credentials") and not (settings.username and settings.password):
        pytest.skip("Chưa có UTC_USER/UTC_PASS hợp lệ trong .env hoặc biến môi trường")
    pass


@pytest.fixture
def browser(settings, case_requirements):
    session = BrowserSession(settings)
    try:
        session.start()
        yield session
    finally:
        session.close()


@pytest.fixture
def login(browser, settings):
    return LoginPage(browser.driver, settings).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if not report.failed or report.when not in {"setup", "call"}:
        return
    session = item.funcargs.get("browser")
    if not session or session.driver is None:
        return
    folder = Path("reports/screenshots")
    folder.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", item.name)
    suffix = hashlib.sha256(item.nodeid.encode()).hexdigest()[:8]
    try:
        # Chụp trước fixture teardown. Lỗi screenshot không che lỗi test gốc.
        png = session.driver.get_screenshot_as_png()
        (folder / f"{name}_{suffix}.png").write_bytes(png)
        extra = getattr(report, "extras", [])
        extra.append(pytest_html.extras.png(session.driver.get_screenshot_as_base64(), name="Screenshot"))
        report.extras = extra
    except Exception as error:
        report.sections.append(("Screenshot", f"Không chụp được ảnh: {type(error).__name__}"))
