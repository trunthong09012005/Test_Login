# UTC Login - Selenium Java

Project tự động hóa 26 test case đăng nhập của trang Văn phòng điện tử UTC theo slide Buổi 8.

- Java, Selenium WebDriver 4, JUnit 5, AssertJ và Gradle Wrapper
- Page Object Model và Explicit Wait, không dùng `Thread.sleep()`
- Headless mặc định; tự chụp ảnh lỗi vào `build/screenshots/`

## Cấu trúc

```text
src/test/java/vn/edu/utc/e2e/
|-- base/       # vòng đời WebDriver và screenshot
|-- config/     # URL, browser và biến môi trường
|-- driver/     # ChromeDriver/EdgeDriver
|-- pages/      # BasePage, LoginPage, HomePage
`-- tests/      # LoginE2ETest - TC1 đến TC26
```

## Chạy

Yêu cầu JDK 17+ và Chrome hoặc Edge. Lần đầu cần Internet để tải Gradle, dependency và driver.

```powershell
.\gradlew.bat test
```

Mặc định không chạy các tag `credential`, `session`, `rate-limit`, `security`.

```powershell
.\gradlew.bat test -Dheadless=false
.\gradlew.bat test -Dbrowser=edge
```

Chạy đủ 26 ca bằng thông tin bí mật từ biến môi trường, không ghi mật khẩu vào source:

```powershell
$env:UTC_USER = "<ten-dang-nhap>"
$env:UTC_PASS = "<mat-khau>"
.\gradlew.bat fullTest
```

Có thể đặt `UTC_LOGIN_URL` và `UTC_PROTECTED_URL` nếu chạy trên môi trường khác. `fullTest` có TC21 thử sai 5 lần và TC24-TC25 kiểm tra payload bảo mật; chỉ chạy khi được phép.

## Nhóm test case

| Nhóm | Test case |
|---|---|
| Validation bắt buộc | TC1, TC2, TC7 |
| Sai thông tin đăng nhập | TC3, TC4, TC8, TC14-TC16 |
| Khoảng trắng/chữ hoa-thường | TC9-TC13 |
| Dữ liệu dài và che mật khẩu | TC17-TC19 |
| Enter và thử sai nhiều lần | TC20-TC21 |
| Phiên, đăng xuất, truy cập bảo vệ | TC5, TC6, TC22, TC23, TC26 |
| SQL Injection/XSS | TC24-TC25 |

## Báo cáo

- HTML: `build/reports/tests/test/index.html`
- JUnit XML: `build/test-results/test/`
- Screenshot khi lỗi: `build/screenshots/`
