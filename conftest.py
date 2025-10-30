# conf test.py ✅
import os
import pytest
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# ---------------------------------------------------------
# Screenshot helper
# ---------------------------------------------------------
def take_screenshot(driver, test_name):
    """
    Take screenshot, save locally with timestamp, and attach to Allure.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, screenshot_name)

    # Save screenshot locally
    driver.save_screenshot(screenshot_path)

    # Attach screenshot to Allure
    with open(screenshot_path, "rb") as f:
        allure.attach(
            f.read(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

    print(f"Screenshot saved: {screenshot_path}")

    return screenshot_path


# ---------------------------------------------------------
# Command-line option to select browser
# ---------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome OR firefox"
    )


# ---------------------------------------------------------
# Browser setup fixture (class-scoped)
# ---------------------------------------------------------
@pytest.fixture(scope="class")
def test_setup(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),  # removed version="latest"
            options=options
        )


    elif browser == "firefox":
        options = FFOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(
            service=FFService(GeckoDriverManager().install()),
            options=options
        )

    else:
        raise ValueError(f"Browser '{browser}' is not supported. Use chrome or firefox.")

    request.cls.driver = driver
    yield
    driver.quit()


# ---------------------------------------------------------
# Pytest hook: capture screenshot on failure
# ---------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # must match hook spec
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # function-level driver
        driver = item.funcargs.get("driver")
        # class-level driver
        if not driver and hasattr(item.instance, "driver"):
            driver = item.instance.driver
        if driver:
            take_screenshot(driver, item.name)
