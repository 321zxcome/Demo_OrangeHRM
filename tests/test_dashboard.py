import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# ---- Fixture ----
@pytest.fixture
def login_dashboard(open_login_page):
    driver = open_login_page
    login_page = LoginPage(driver)
    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login()
    return DashboardPage(driver)

# ---- Test Class ----
@pytest.mark.usefixtures("open_login_page")
class TestDashboard:

    @pytest.mark.parametrize(
        ("ID", "case", "data", "action", "expected"),
        [
            ("DB_1", "Login page Dashboard", None, "dashboard_loaded", True),
            ("DB_2", "Verify Dashboard page title", None, "get_title", "Dashboard"),
            ("DB_4", "Verify Logo", None, "dashboard_logo", True),
            ("DB_5", "Verify breadcrumb", None, "dashboard_breadcrumb", "Dashboard"),
        ]
    )
    def test_dashboard_case(self, login_dashboard, ID, case, data, action, expected):
        # Call method dynamically; pass data if provided
        result = getattr(login_dashboard, action)(*data) if data else getattr(login_dashboard, action)()

        # Check result depending on type (boolean or text)
        if isinstance(expected, bool):
            assert result == expected, f"{ID} - {case} failed, result: {result}"
        else:
            assert expected in str(result), f"{ID} - {case} failed, result: {result}"

        print(f"{ID} - {case}: passed")

    # ---- Menu Toggle ----
    # DB6: Verify button toggle menu
    def test_menu_toggle(self, login_dashboard):
        text_case = "DB6: Verify button toggle menu"
        # Get menu and toggle button
        menu, toggle_btn = login_dashboard.verify_menu()

        # Check menu
        assert menu.is_displayed(), "Menu is not displayed"

        # Open menu
        toggle_btn.click()
        login_dashboard.wait.until(
            # EC.text_to_be_present_in_element_attribute(locator, attribute, text)
            EC.text_to_be_present_in_element_attribute((By.CLASS_NAME, "oxd-sidepanel"), "class", "toggled")
        )
        time.sleep(1)
        assert "toggled" in menu.get_attribute("class"), f"{text_case} - Fail: Menu did not toggle open"
        print("{text_case} - Pass: Menu toggled open successfully")

        # Close menu
        toggle_btn.click()
        login_dashboard.wait.until_not(
            EC.text_to_be_present_in_element_attribute((By.CLASS_NAME, "oxd-sidepanel"), "class", "toggled")
        )
        time.sleep(1)
        assert "toggled" not in menu.get_attribute("class"), "{text_case} - Fail: Menu did not toggle closed"
        print("{text_case} - Pass: Menu toggled closed successfully")

    # ---- Search Bar ----
    @pytest.mark.parametrize(
        ("ID", "case", "keyword", "count"),
        [
            ("DB_7", "Verify search bar", "admin", 1),
            ("DB_8", "Verify empty search", "zzz123", 0),
        ]
    )
    def test_search_bar(self, login_dashboard, ID, case, keyword, count):
        # Search keyword
        login_dashboard.search_dashboard(keyword)
        time.sleep(1)

        # Search results
        items = login_dashboard.search_result_items()
        assert len(items) >= count, f"{ID} - {case} failed: Expected at least {count} results, got {len(items)}"
        print(f"{ID} - {case}: passed")

    # ---- Widget Tests ----
    @pytest.mark.parametrize(
        ("ID", "case", "name", "click_btn", "num"),
        [
            ("DB_9", "Quick Launch", "quick_launch", True, 6),
            ("DB_10", "Time at Work", "time_at_work", True, 1),
            ("DB_11", "My Actions", "my_actions", True, 2)
        ]
    )
    def test_widgets(self, login_dashboard, ID, case, name, click_btn, num):
        # Check widget visibility
        btn_visible = login_dashboard.get_widget_visible(name)
        assert btn_visible, f"{ID} - {case}: Widget {btn_visible} not visible"

        # ---- Quick Launch ----
        if name == "quick_launch":
            btn_quick = login_dashboard.get_quick_btn()
            # Count buttons
            assert len(btn_quick) == num, f"Display {len(btn_quick)} - expected {num}"
            # Click all buttons
            for i, btn in enumerate(btn_quick):
                assert btn.is_displayed(), f"Button {i} invisible"
                btn.click()
                # Back to the previous page
                login_dashboard.driver.back()

        # ---- Time at Work ----
        elif name == "time_at_work":
            # Check punch status
            punch_stt = login_dashboard.get_punch_status()
            assert punch_stt is not None, f"{ID} - {case}: Punch In/Out status missing"

            # Check total time
            total_time = login_dashboard.get_total_time()
            assert total_time, f"{ID} - {case}: Total time missing"

            # Check chart 
            chart_time = login_dashboard.get_chart()
            assert len(chart_time) >= 1, f"{ID} - {case}: Chart invisible"

            # Click all Time buttons
            btn_time = login_dashboard.get_btn_time()
            assert len(btn_time) == num, f"Display {len(btn_time)} - expected {num}"
            for i, btn in enumerate(btn_time):
                assert btn.is_displayed(), f"Button {i} invisible"
                btn.click()
                login_dashboard.driver.back()

        # ---- My Actions ----
        elif name == "my_actions":
            items = login_dashboard.get_my_action_items()
            assert len(items) == num, f"Action: {len(items)}, expected: {num}"
            for i, item in enumerate(items):
                assert item.is_displayed(), f"Button {i} invisible"
                item.click()
                login_dashboard.driver.back()

        print(f"{ID} - {case}: passed")
