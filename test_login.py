from selenium import webdriver
from selenium.webdriver.chrome.service import Service

browser_path = 'D:/chrome-win64/chrome-win64/chrome.exe'
driver_path = 'D:/chromedriver-win64/chromedriver-win64/chromedriver.exe'
import pytest
from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By
url = "http://practice.automationtesting.in/"

@pytest.fixture(scope='module')
def setup():
    op = webdriver.ChromeOptions()
    op.binary_location = browser_path
    op.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=op, service=Service(executable_path=driver_path))
    driver.maximize_window()
    driver.get(url=url)
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def conditions(setup):
    driver = setup
    driver.find_element(By.LINK_TEXT, 'My Account').click()

def test_login_with_valid_username_and_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("burhan.jamil50@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Qwerty7@1234...")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    actual_logout_ext = driver.find_element(By.LINK_TEXT, "Logout").text
    assert "Logout" == actual_logout_ext
    driver.find_element(By.LINK_TEXT, "Logout").click()

def test_login_with_invalid_username_and_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("burhan.jamil5000000@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Qwerty7@1234777")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    error = driver.find_element(By.CLASS_NAME, "woocommerce-error")
    assert "Error:" == error.find_element(By.TAG_NAME, "Strong").text


def test_login_with_valid_username_and_empty_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("burhan.jamil50@gmail.com")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    error = driver.find_element(By.CLASS_NAME, "woocommerce-error")
    assert error.text.__contains__("Password is required")


def test_login_with_empty_username_and_valid_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("Qwerty7@1234...")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    error = driver.find_element(By.CLASS_NAME, "woocommerce-error")
    assert error.text.__contains__("Username is required")

@pytest.mark.xfail
def test_login_with_empty_username_and_empty_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    error = driver.find_element(By.CLASS_NAME, "woocommerce-error")
    assert error.text.__contains__("Username is required")


def test_login_password_should_be_masked(setup):
    driver = setup
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("123456")
    assert "password" == password_field.get_attribute("type")


@pytest.mark.skip
def test_login_with_case_changed(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("Burhan.jamil50@gmail.com")
    driver.find_element(By.ID, "password").send_keys("qwerty7@1234")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    error_label = driver.find_element(By.TAG_NAME, "Strong").text
    assert "Error:" == error_label


@pytest.mark.xfail
def test_login_with_authentication(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("burhan.jamil50@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Qwerty7@1234")
    driver.find_element(By.XPATH, "//*[@id='customer_login']/div[1]/form/p[3]/input[3]").click()
    driver.find_element(By.LINK_TEXT, "Logout").click()
    driver.back()
    try:
        driver.find_element(By.LINK_TEXT, "Logout")
        assert False
    except NoSuchElementException as e:
        assert True