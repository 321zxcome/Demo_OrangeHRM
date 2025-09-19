from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    logo_header = (By.CLASS_NAME, "oxd-brand")
    breadcrumb_header = (By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module")
    search_input = (By.CSS_SELECTOR, "input[placeholder='Search']")
    search_result = (By.XPATH, "//ul[@class='oxd-main-menu']")
    WIDGETS = {
        "time_at_work": (By.XPATH, "//p[text()='Time at Work']"),
        "my_actions": (By.XPATH, "//p[text()='My Actions']"),
        "quick_launch": (By.XPATH, "//p[text()='Quick Launch']"),
        "buzz_post": (By.XPATH, "//p[text()='Buzz Latest Posts']"),
        "leave_today": (By.XPATH, "//p[text()='Employees on Leave Today']"),
        "chart_unit": (By.XPATH, "//p[text()='Employee Distribution by Sub Unit']"),
        "chart_location": (By.XPATH, "//p[text()='Employee Distribution by Location']"),
    }
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def dashboard_loaded(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.DASHBOARD_HEADER)
        ).is_displayed()

    def get_title(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.DASHBOARD_HEADER)
        ).text

    def dashboard_logo(self):
        return self.driver.find_element(*self.logo_header).is_displayed()

    def dashboard_breadcrumb(self):
        return self.wait.until(EC.visibility_of_element_located(self.breadcrumb_header)).text

    def verify_menu(self):
        menu = self.driver.find_element(By.CLASS_NAME,"oxd-sidepanel")
        toggle_btn = self.driver.find_element(By.CLASS_NAME, "oxd-main-menu-button")
        return menu, toggle_btn

    def search_dashboard(self, keyword: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.search_input)
        )
        search_input.clear()
        search_input.send_keys(keyword)

    def search_result_items(self):
        result = self.wait.until(
            EC.presence_of_element_located(self.search_result)
        )
        items = result.find_elements(By.TAG_NAME, "li")
        return items

    def get_widget_visible(self, name: str):
        locator = self.WIDGETS.get(name)
        if not locator:
            raise ValueError(f"No widget named '{name}'")
        return self.wait.until(
            EC.visibility_of_element_located(locator).is_displayed()
        )