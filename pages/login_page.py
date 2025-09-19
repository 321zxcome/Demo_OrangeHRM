from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Page Object Model cho trang login OrangeHRM
    Bao gồm:
    - Login
    - Forgot Password
    - Kiểm tra UI
    """

    def __init__(self, driver):
        self.driver = driver

        # =====================
        # Locators cho Login
        # =====================
        self.username_input = (By.NAME, "username")               # Ô nhập Username
        self.password_input = (By.NAME, "password")               # Ô nhập Password
        self.login_button = (By.XPATH, "//button[@type='submit']") # Nút Login
        self.error_message = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]") # Thông báo lỗi

        # =====================
        # Locators cho Forgot Password
        # =====================
        self.forgot_password_link = (By.XPATH, "//p[contains(text(),'Forgot your password?')]")  # Link Forgot
        self.email_input = (By.NAME, "email")                 # Ô nhập email
        self.reset_password_button = (By.XPATH, "//button[text()='Reset Password']")  # Nút Reset
        self.reset_success_message = (By.XPATH, "//p[contains(text(),'successfully')]")  # Thông báo thành công

        # =====================
        # Locator cho logo UI check
        # =====================
        self.logo = (By.CSS_SELECTOR, "div.orangehrm-login-branding img")

    # =====================
    # Methods Login
    # =====================
    def enter_username(self, username):
        """
        Nhập username vào ô input
        """
        field = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.username_input)
        )
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        """
        Nhập password vào ô input
        """
        field = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.password_input)
        )
        field.clear()
        field.send_keys(password)

    def click_login(self):
        """
        Click nút login khi có thể click được
        """
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def get_error_message(self):
        """
        Lấy text thông báo lỗi khi login thất bại
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message)
        ).text

    # =====================
    # Methods Forgot Password
    # =====================
    def click_forgot_password(self):
        """
        Click link 'Forgot your password?'
        """
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.forgot_password_link)
        ).click()

    def enter_email(self, email):
        """
        Nhập email để reset password
        """
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input)
        )
        field.clear()
        field.send_keys(email)

    def click_reset_password(self):
        """
        Click nút Reset Password
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.reset_password_button)
        ).click()

    def get_reset_success_message(self):
        """
        Lấy thông báo thành công reset password
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.reset_success_message)
        ).text

    # =====================
    # Methods UI check
    # =====================
    def is_username_displayed(self):
        """
        Kiểm tra username field có hiển thị không
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).is_displayed()

    def is_password_displayed(self):
        """
        Kiểm tra password field có hiển thị không
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        ).is_displayed()

    def is_login_button_displayed(self):
        """
        Kiểm tra login button có hiển thị không
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.login_button)
        ).is_displayed()

    def is_logo_displayed(self):
        """
        Kiểm tra logo có hiển thị không
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.logo)
        ).is_displayed()