# utils.py

import os
import inspect
from datetime import datetime
import allure
from selenium.webdriver.remote.webdriver import WebDriver

# =========================
# ✅ CONSTANTS
# =========================
URL = "https://opensource-demo.orangehrmlive.com/"
USERNAME = "Admin"
PASSWORD = "admin123"


# =========================
# ✅ HELPER FUNCTIONS
# =========================
def whoami() -> str:
    """Return the name of the calling function (used as test name)."""
    return inspect.stack()[1][3]


def take_screenshot(driver: WebDriver, test_name: str) -> None:
    """Attach screenshot to Allure and save locally with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{test_name}_{timestamp}"
    screenshot_path = f"C:/Users/abyja/PycharmProjects/Automation_Framework_NG/screenshots/{screenshot_name}.png"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

    # Attach to Allure
    allure.attach(
        driver.get_screenshot_as_png(),
        name=screenshot_name,
        attachment_type=allure.attachment_type.PNG
    )

    # Save locally
    driver.get_screenshot_as_file(screenshot_path)
