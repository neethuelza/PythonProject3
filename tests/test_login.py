import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver

from pages.loginPage import LoginPage
from pages.homePage import HomePage
from utils import utils


@pytest.mark.usefixtures("test_setup")
class TestLogin:
    driver: WebDriver

    def test_login(self):
        """Test for logging in and verifying the dashboard title"""
        driver = self.driver
        driver.get(utils.URL)

        login = LoginPage(driver)
        login.enter_username(utils.USERNAME)
        login.enter_password(utils.PASSWORD)
        login.click_login()

        WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']"))
        )

        # If this fails, pytest hook will automatically take screenshot
        assert driver.title == "OrangeHRM"

    def test_logout(self):
        """Test for logging out from the application"""
        driver = self.driver
        home = HomePage(driver)

        home.click_dashboard_title()
        home.click_profile_dropdown()
        home.click_logout_button()
