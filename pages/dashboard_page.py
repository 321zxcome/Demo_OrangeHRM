from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    # ---- Locators ----
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    LOGO_HEADER = (By.CLASS_NAME, "oxd-brand")
    BREADCRUMB_HEADER = (By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")
    SEARCH_RESULT = (By.XPATH, "//ul[@class='oxd-main-menu']")
    TITLE_WIDGETS = (By.CSS_SELECTOR, "p.oxd-text.oxd-text--p")  

    # Widget locators
    WIDGETS = {
        "time_at_work": (By.XPATH, "//p[text()='Time at Work']"),
        "my_actions": (By.XPATH, "//p[text()='My Actions']"),
        "quick_launch": (By.XPATH, "//p[text()='Quick Launch']"),
        "buzz_post": (By.XPATH, "//p[text()='Buzz Latest Posts']"),
        "leave_today": (By.XPATH, "//p[text()='Employees on Leave Today']"),
        "chart_unit": (By.XPATH, "//p[text()='Employee Distribution by Sub Unit']"),
        "chart_location": (By.XPATH, "//p[text()='Employee Distribution by Location']"),
    }

    # Quick Launch buttons
    QUICK_BTN = (By.CLASS_NAME, "orangehrm-quick-launch-icon")
    # My Actions items
    MY_ACTION_ITEMS = (By.CSS_SELECTOR, ".orangehrm-todo-list-item")

    # Time at Work elements
    TIME_BTN = (By.CLASS_NAME, "orangehrm-attendance-card-action")
    PUNCH_STATUS = (By.CSS_SELECTOR, ".orangehrm-attendance-card-profile-record .orangehrm-attendance-card-details")
    TOTAL_TIME = (By.CSS_SELECTOR, ".orangehrm-attendance-card-bar .orangehrm-attendance-card-fulltime")
    CHART_CANVAS = (By.CSS_SELECTOR, ".emp-attendance-chart canvas")
    
    # ---- Constructor ----
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---- Dashboard Basic Checks ----
    def dashboard_loaded(self):
        # Wait until dashboard header is visible
        return self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER)).is_displayed()

    def get_title(self):
        # Return the dashboard page title text
        return self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER)).text

    def dashboard_logo(self):
        # Check if logo is displayed
        element = self.driver.find_element(*self.LOGO_HEADER)
        return element.is_displayed()

    def dashboard_breadcrumb(self):
        # Return breadcrumb text
        return self.wait.until(EC.visibility_of_element_located(self.BREADCRUMB_HEADER)).text

    # ---- Menu ----
    def verify_menu(self):
        # Return menu panel and toggle button
        menu = self.driver.find_element(By.CLASS_NAME,"oxd-sidepanel")
        toggle_btn = self.driver.find_element(By.CLASS_NAME, "oxd-main-menu-button")
        return menu, toggle_btn

    # ---- Search ----
    def search_dashboard(self, keyword: str):
        # Enter keyword in search input
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(keyword)

    def search_result_items(self):
        # Return all li items in search result
        result = self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULT))
        return result.find_elements(By.TAG_NAME, "li")

    # ---- Widget Checks ----
    def get_widget_visible(self, name: str):
        # Check if widget is displayed
        locator = self.WIDGETS.get(name)
        if not locator:
            raise ValueError(f"No widget named '{name}'")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.is_displayed()

    # ---- Quick Launch ----
    def get_quick_btn(self):
        # Return all quick launch buttons
        return self.driver.find_elements(*self.QUICK_BTN)

    def click_btn_widgets(self, index: int):
        # Click a specific Quick Launch button by index
        btn_widgets = self.get_quick_btn()
        if index < 0 or index >= len(btn_widgets):
            raise ValueError("Quick Launch index out of range")
        btn_widgets[index].click()

    # ---- Title Widgets ----
    def get_title_widgets(self):
        # Return list of all widget titles
        elements = self.wait.until(EC.presence_of_all_elements_located(self.TITLE_WIDGETS))
        return [el.text for el in elements]

    # ---- Time at Work ----
    def get_punch_status(self):
        # Return Punch In/Out status text
        stt = self.driver.find_element(*self.PUNCH_STATUS)
        return stt.text
    
    def get_total_time(self):
        # Return total work time text
        total = self.driver.find_element(*self.TOTAL_TIME)
        return total.text.strip()
    
    def get_chart(self):
        # Return all chart canvas elements
        return self.driver.find_elements(*self.CHART_CANVAS)

    def get_btn_time(self):
        # Return all Time at Work action buttons
        return self.driver.find_elements(*self.TIME_BTN)

    # ---- My Actions ----
    def get_my_action_items(self):
        # Return all My Actions items
        return self.driver.find_elements(*self.MY_ACTION_ITEMS)

    # ---- Generic Click Helper ----
    def click_all_visible_btn(self, elements):
        # Click all displayed elements in a list.
        count = 0
        for el in elements:
            if el.is_displayed():
                el.click()
                # Wait until element is displayed again to avoid StaleElementReferenceException
                self.wait.until(lambda d: el.is_displayed())
                count += 1
        return count

    def click_all_btn_time(self):
        # Click all visible Time at Work buttons
        btns = self.get_btn_time()
        return self.click_all_visible_btn(btns)

    def click_btn_action(self):
        # Click all visible My Actions items
        items = self.get_my_action_items()
        return self.click_all_visible_btn(items)
