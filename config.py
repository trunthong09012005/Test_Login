"""Cấu hình dùng chung; mật khẩu chỉ lấy từ môi trường hoặc .env."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
DEFAULT_LOGOUT = "a[href*='/Logout'], a[href*='/logout'], a[href*='/SignOut']"


def _optional_positive_int(name: str) -> int | None:
    value = os.getenv(name, "").strip()
    if not value:
        return None
    number = int(value)
    if number < 1:
        raise ValueError(f"{name} phải là số nguyên dương")
    return number


@dataclass(frozen=True)
class Settings:
    login_url: str
    protected_url: str
    username: str
    password: str = field(repr=False)
    invalid_message: str
    username_whitespace: str
    username_case: str
    session_after_restart: str
    authenticated_css: str
    logout_css: str
    username_max_length: int | None
    password_max_length: int | None
    lockout_after: int | None
    lockout_message: str
    browser: str
    headless: bool
    timeout: float

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv(ROOT / ".env", override=False)
        login_url = os.getenv("UTC_LOGIN_URL", "https://vanphongdientu.utc.edu.vn/Login")
        origin = urlparse(login_url)
        instance = cls(
            login_url=login_url,
            protected_url=os.getenv("UTC_PROTECTED_URL", f"{origin.scheme}://{origin.netloc}/"),
            username=os.getenv("UTC_USER", "huongnt"),
            password=os.getenv("UTC_PASS", ""),
            invalid_message=os.getenv("UTC_INVALID_MESSAGE", "Tài khoản không đúng"),
            username_whitespace=os.getenv("UTC_USERNAME_WHITESPACE", "").lower(),
            username_case=os.getenv("UTC_USERNAME_CASE", "").lower(),
            session_after_restart=os.getenv("UTC_SESSION_AFTER_RESTART", "login").lower(),
            authenticated_css=os.getenv("UTC_AUTHENTICATED_CSS", DEFAULT_LOGOUT),
            logout_css=os.getenv("UTC_LOGOUT_CSS", DEFAULT_LOGOUT),
            username_max_length=_optional_positive_int("UTC_USERNAME_MAX_LENGTH"),
            password_max_length=_optional_positive_int("UTC_PASSWORD_MAX_LENGTH"),
            lockout_after=_optional_positive_int("UTC_LOCKOUT_AFTER"),
            lockout_message=os.getenv("UTC_LOCKOUT_MESSAGE", ""),
            browser=os.getenv("BROWSER", "chrome").lower(),
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            timeout=float(os.getenv("WAIT_TIMEOUT", "15")),
        )
        instance.validate()
        return instance

    def validate(self) -> None:
        for value in (self.login_url, self.protected_url):
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("URL kiểm thử phải là địa chỉ HTTP/HTTPS hợp lệ")
        if self.browser not in {"chrome", "edge"}:
            raise ValueError("BROWSER phải là chrome hoặc edge")
        if self.timeout <= 0:
            raise ValueError("WAIT_TIMEOUT phải lớn hơn 0")
        if self.username_whitespace not in {"", "trim", "reject"}:
            raise ValueError("UTC_USERNAME_WHITESPACE phải là trim hoặc reject")
        if self.username_case not in {"", "insensitive", "sensitive"}:
            raise ValueError("UTC_USERNAME_CASE phải là insensitive hoặc sensitive")
        if self.session_after_restart not in {"login", "authenticated"}:
            raise ValueError("UTC_SESSION_AFTER_RESTART phải là login hoặc authenticated")
        if not self.authenticated_css or not self.logout_css or not self.invalid_message:
            raise ValueError("Selector và thông báo lỗi mong đợi không được trống")
        if self.lockout_after and not self.lockout_message:
            raise ValueError("Cần UTC_LOCKOUT_MESSAGE khi cấu hình UTC_LOCKOUT_AFTER")
