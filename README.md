# UTC Login - Selenium Python (Pytest)

Project tự động hóa 26 test case đăng nhập của trang Văn phòng điện tử UTC. Đã được chuyển đổi hoàn toàn từ nền tảng Java sang Python!

- Ngôn ngữ & Framework: Python 3, Selenium WebDriver 4, Pytest, Python-dotenv.
- Kiến trúc: Áp dụng **Page Object Model (POM)** và **Explicit Wait** (chờ đợi thông minh).
- Tính năng: Hỗ trợ chạy ẩn (headless), tự chụp ảnh lỗi, xuất báo cáo HTML và xuất kết quả ra file Excel.

## Cấu trúc Dự Án

```text
Test_Login/
|-- pages/              # Các Page Object (BasePage, LoginPage, HomePage)
|-- tests/              # Thư mục chứa các kịch bản kiểm thử (test_login.py chứa 26 TC)
|-- utils/              # Cấu hình Browser Session
|-- reports/            # Nơi lưu báo cáo HTML, XML, ảnh chụp lỗi và file Excel
|-- config.py           # Thiết lập cấu hình hệ thống
|-- conftest.py         # Cấu hình Pytest, setup/teardown Fixtures (browser, login, ...)
|-- pytest.ini          # Tùy chỉnh Pytest
|-- export_excel.py     # Script tự động lấy kết quả log xuất ra file Excel (.xlsx)
`-- requirements.txt    # Danh sách thư viện Python cần cài đặt
```

## Hướng Dẫn Chạy

1. **Cài đặt các thư viện cần thiết:**
```bash
pip install -r requirements.txt
pip install openpyxl
```

2. **Cấu hình tài khoản:**
Tạo file `.env` ở thư mục gốc (hoặc copy từ `.env.example`) và điền tài khoản để test:
```env
UTC_LOGIN_URL=https://vanphongdientu.utc.edu.vn/Login
UTC_PROTECTED_URL=https://vanphongdientu.utc.edu.vn/
UTC_USER=<tên_đăng_nhập_của_bạn>
UTC_PASS=<mật_khẩu_của_bạn>
```

3. **Chạy toàn bộ 26 kịch bản (có hiển thị giao diện):**
```bash
python -m pytest tests/ --headed
```
*(Nếu muốn chạy ẩn ngầm dưới nền cho tốc độ cực nhanh, hãy bỏ cờ `--headed` đi)*.

4. **Xuất báo cáo ra file Excel:**
```bash
python export_excel.py
```
*(File Excel sẽ được lưu tại `reports/Test_Results_v2.xlsx` với định dạng cực kỳ chuyên nghiệp).*

---

## 📊 Báo cáo Kết Quả Kiểm Thử (Cập nhật mới nhất)

**Tổng quan:**
- **Tổng số Test Cases:** 26
- **Pass (Xanh):** 21
- **Failed (Đỏ):** 5
- **Tổng thời gian chạy:** ~9 phút 18 giây

**Chi tiết các Test Case Failed:**
Các test case bị lỗi (Failed) bao gồm: `TC05`, `TC06`, `TC20`, `TC22`, `TC26`. 

**Nguyên nhân gốc rễ (Root Cause):**
- Cả 5 test case bị Failed này đều thuộc nhóm **"Yêu cầu Đăng nhập thành công"** (Kỳ vọng: sau khi click Login, hệ thống sẽ chuyển hướng vào Trang chủ Dashboard/Protected).
- Tuy nhiên, trong quá trình chạy tự động, thông tin tài khoản test đã bị từ chối hoặc hệ thống không ghi nhận đăng nhập thành công, khiến trình duyệt vẫn bị kẹt ở trang Login ban đầu -> Dẫn tới Assertion Failed.
- **Tất cả 21 test case còn lại** (Nhóm cố tình nhập sai thông tin, bỏ trống ô, nhập quá độ dài, tấn công SQL Injection...) đều **PASSED 100%**. Hệ thống đã hiển thị chính xác các thông báo lỗi cảnh báo hoàn toàn khớp với kịch bản mong đợi!

### Bảng Chi Tiết Kết Quả 26 Test Cases

| STT | Mã TC | Phân loại | Mô tả | Trạng thái |
|:---:|:---:|:---:|---|:---:|
| 1 | **TC01** | Negative | Để trống tên đăng nhập | ✅ **PASSED** |
| 2 | **TC02** | Negative | Để trống mật khẩu | ✅ **PASSED** |
| 3 | **TC03** | Negative | Đúng Username, sai Password | ✅ **PASSED** |
| 4 | **TC04** | Negative | Sai Username, đúng Password | ✅ **PASSED** |
| 5 | **TC05** | Positive | Đăng nhập chọn 'Giữ tôi luôn đăng nhập' | ❌ **FAILED** |
| 6 | **TC06** | Positive | Đăng nhập không chọn giữ đăng nhập | ❌ **FAILED** |
| 7 | **TC07** | Negative | Để trống cả Username và Password | ✅ **PASSED** |
| 8 | **TC08** | Negative | Sai cả Username và Password | ✅ **PASSED** |
| 9 | **TC09** | Negative | Username có khoảng trắng ở đầu | ✅ **PASSED** |
| 10 | **TC10** | Negative | Username có khoảng trắng ở cuối | ✅ **PASSED** |
| 11 | **TC11** | Negative | Password có khoảng trắng ở đầu | ✅ **PASSED** |
| 12 | **TC12** | Negative | Password có khoảng trắng ở cuối | ✅ **PASSED** |
| 13 | **TC13** | Negative | Username viết hoa toàn bộ | ✅ **PASSED** |
| 14 | **TC14** | Negative | Password sai chữ hoa/thường | ✅ **PASSED** |
| 15 | **TC15** | Negative | Username chứa ký tự đặc biệt | ✅ **PASSED** |
| 16 | **TC16** | Negative | Password chứa ký tự đặc biệt | ✅ **PASSED** |
| 17 | **TC17** | Negative | Username dài 256 ký tự | ✅ **PASSED** |
| 18 | **TC18** | Negative | Password dài 256 ký tự | ✅ **PASSED** |
| 19 | **TC19** | Positive | Mật khẩu được che khi nhập | ✅ **PASSED** |
| 20 | **TC20** | Positive | Đăng nhập bằng phím Enter | ❌ **FAILED** |
| 21 | **TC21** | Negative | Đăng nhập sai 5 lần liên tiếp | ✅ **PASSED** |
| 22 | **TC22** | Positive | Đăng xuất sau khi đăng nhập | ❌ **FAILED** |
| 23 | **TC23** | Negative | Truy cập trang bảo vệ khi chưa đăng nhập | ✅ **PASSED** |
| 24 | **TC24** | Negative | SQL Injection vào form | ✅ **PASSED** |
| 25 | **TC25** | Negative | XSS Injection vào form | ✅ **PASSED** |
| 26 | **TC26** | Positive | Nút Back không khôi phục phiên | ❌ **FAILED** |
