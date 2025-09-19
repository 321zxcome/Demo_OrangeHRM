import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture
def login_dashboard(open_login_page):
    driver = open_login_page
    login_page = LoginPage(driver)
    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()
    return DashboardPage(driver)

@pytest.mark.usefixtures("open_login_page")
class TestDashboard:

    @pytest.mark.parametrize(
        ("ID", "case", "data", "action", "expected"),
        [
            ("DB_1", "Login page Dashboard", None, "dashboard_loaded", True),
            ("DB_2","Verify Dashboard page title", None, "get_title", "Dashboard"),
            ("DB_4","Verify Logo", None, "dashboard_logo", True),
            ("DB_5", "Verify breadcrumb", None, "dashboard_breadcrumb", "Dashboard"),
        ]
    )
    def test_dashboard_case(self, login_dashboard, ID, case, data, action, expected):
        # Gọi method với hoặc không có argument
        result = getattr(login_dashboard, action)(*data) if data else getattr(login_dashboard, action)()

        # So sánh kết quả
        if isinstance(expected, bool):
            assert result == expected, f"{ID} - {case} failed, result: {result}"
        else:
            assert expected in str(result), f"{ID} - {case} failed, result: {result}"

        print(f"{ID} - {case}: passed")

    # DB6: Verify button toggle menu
    def test_menu_toggle(self, login_dashboard):
        menu, toggle_btn = login_dashboard.verify_menu()
        # check menu
        assert menu.is_displayed(), "menu is not displayed"
        # open menu
        toggle_btn.click()
        login_dashboard.wait.until(
            # EC.text_to_be_present_in_element_attribute(locator, attribute, text)
            EC.text_to_be_present_in_element_attribute((By.CLASS_NAME, "oxd-sidepanel"), "class", "toggled")
        )
        time.sleep(1)
        assert "toggled" in menu.get_attribute("class"),  "Fail: Menu did not toggle open"
        print("Pass: Menu toggled open successfully")
        # close menu
        toggle_btn.click()
        login_dashboard.wait.until_not(
            EC.text_to_be_present_in_element_attribute((By.CLASS_NAME, "oxd-sidepanel"), "class", "toggled")
        )
        time.sleep(1)
        assert "toggled" not in menu.get_attribute("class"), "Fail: Menu did not toggle closed"
        print("Pass: Menu toggled closed successfully")


    @pytest.mark.parametrize(
        ("ID", "case", "keyword", "count"),
        [
            ("DB_7", "Verify search bar", "admin", 1),
            ("DB_8", "Verify empty search", "zzz123", 0),
        ]
    )
    def test_search_bar(self, login_dashboard, ID, case, keyword, count):
        login_dashboard.search_dashboard(keyword)
        time.sleep(1)
        items = login_dashboard.search_result_items()
        assert len(items) >= count,f"{ID} - {case} failed: Expected at least {count} results, got {len(items)}"
        print(f"{ID} - {case}: passed")