import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage

@pytest.mark.usefixtures("open_login_page")
class TestLogin:

    # --- Success case ---
    def test_login_success(self, open_login_page, request):
        driver = open_login_page
        login_page = LoginPage(driver)

        login_page.enter_username("Admin")
        login_page.enter_password("admin123")
        login_page.click_login()

        dashboard = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )
        assert dashboard.is_displayed(), "page not found"
        print(f"{request.node.name}: Pass (successful login)")

    # --- Invalid cases gộp lại ---
    @pytest.mark.parametrize(
        "username,password,expected_error,case_name",
        [
            ("WrongUser123", "admin123", "Invalid credentials", "Invalid Username"),
            ("Admin", "wrongpass", "Invalid credentials", "Invalid Password"),
            ("", "", "Required", "Empty Username & Password"),
            ("a"*101, "admin123", "Invalid credentials", "Too Long Username"),
            ("Admin", "a"*51, "Invalid credentials", "Too Long Password"),
            ("Adm", "admin123", "Invalid credentials", "Too Short Username"),
            ("Admin", "short", "Invalid credentials", "Too Short Password"),
            ("!@#$%", "^&*()", "Invalid credentials", "Special Characters"),
            ("admin", "Admin123", "Invalid credentials", "Case Sensitive"),
        ]
    )
    def test_invalid_login(self, open_login_page, request, username, password, expected_error, case_name):
        driver = open_login_page
        login_page = LoginPage(driver)

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()

        # Chọn locator theo loại lỗi
        if expected_error == "Required":
            locator = (By.XPATH, "//span[text()='Required']")
        else:
            locator = (By.XPATH, "//div[@class='oxd-alert-content oxd-alert-content--error']")

        error_elm = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        error_msg = error_elm.text

        assert expected_error in error_msg
        # In ra rõ tên test case + message
        print(f"{request.node.name} | {case_name}: Pass (error massage: {error_msg})")
