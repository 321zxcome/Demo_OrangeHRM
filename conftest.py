import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Thư mục lưu screenshot ---
SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# --- File lưu report ---
REPORT_FILE = os.path.join(os.getcwd(), "report.txt")


@pytest.fixture
def driver(request):
    """
    Fixture tạo Chrome WebDriver cho mỗi test case.
    - Mở Chrome
    - Maximize window
    - implicit wait 5s
    - Teardown: đóng browser + chụp screenshot nếu test fail
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver   # trả driver cho test case

    # --- Teardown sau khi test chạy ---
    # Nếu test FAIL -> chụp screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")

    driver.quit()  # luôn đóng browser sau mỗi test


# --- Hook: lưu kết quả test (pass/fail) ---
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Hook của pytest: lưu kết quả test (setup/call/teardown) vào item.
    Dùng trong fixture driver để biết test pass/fail.
    Đồng thời log vào file report.txt
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call":  # chỉ log khi chạy test chính
        if rep.passed:
            status = "PASSED"
        elif rep.failed:
            status = "FAILED"
        elif rep.skipped:
            status = "SKIPPED"
        else:
            status = "UNKNOWN"

        test_name = item.name
        log_line = f"{test_name} → {status}"
        print(log_line)

        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")


# --- Fixture mở trang login ---
@pytest.fixture
def open_login_page(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    return driver


# --- Fixture dữ liệu hợp lệ ---
@pytest.fixture
def valid_credentials():
    return {"username": "Admin", "password": "admin123"}


# --- Fixture dữ liệu sai username ---
@pytest.fixture
def invalid_username():
    return {"username": "WrongUser", "password": "admin123"}


# --- Fixture dữ liệu sai password ---
@pytest.fixture
def invalid_password():
    return {"username": "Admin", "password": "wrongpass"}
