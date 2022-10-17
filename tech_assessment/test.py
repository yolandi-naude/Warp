from _pytest.outcomes import fail
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver_path = ChromeDriverManager().install()

def start_driver():
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(3)
    return driver

def login_as_test_user(driver):
    driver.get('http://recruitment.warpdevelopment.co.za/')
    driver.find_element(By.ID,'Email').send_keys('test@warpdevelopment.com')
    driver.find_element(By.ID,'Password').send_keys('123')
    driver.find_element(By.XPATH,'//input[@type="submit"]').click()


def test_order_items():
    driver = start_driver()
    login_as_test_user(driver)

    driver.find_element(By.NAME,'q').send_keys('unpublished product')
    driver.find_element(By.XPATH,'//input[@value="Search"]').click()

    driver.find_element(By.LINK_TEXT, 'Unpublished Product').click()

    driver.find_element(By.NAME,'Qty').send_keys('4')
    driver.find_element(By.XPATH,'//input[@value="Order"]').click()

    expected_message = 'Success'
    actual_message = driver.find_element(By.TAG_NAME, 'h2').text
    if actual_message != expected_message:
        driver.save_screenshot('screenshots/success_message.png')
        driver.quit()
        fail(f'Expected message is "{expected_message}", but actual was: "{actual_message}"')
    driver.quit()


def test_invalid_order():
    driver = start_driver()
    login_as_test_user(driver)

    driver.find_element(By.NAME,'q').send_keys('unpublished product')
    driver.find_element(By.XPATH,'//input[@value="Search"]').click()

    driver.find_element(By.LINK_TEXT, 'Unpublished Product').click()

    driver.find_element(By.NAME,'Qty').send_keys('20')
    driver.find_element(By.XPATH, '//input[@value="Order"]').click()

    actual_message = driver.find_element(By.XPATH, '//div[@class ="validation-summary-errors text-danger" ]').text
    expected_message= 'Out of stock.'
    if actual_message != expected_message:
        driver.save_screenshot('screenshots/order_message.png')
        driver.quit()
        fail(f'Expected message is "{expected_message}", but actual was: "{actual_message}"')
    driver.quit()

def test_placeholder_text():
    driver = start_driver()
    login_as_test_user(driver)

    expected_placeholder = 'Search for product'
    actual_placeholder = driver.find_element(By.NAME, 'q').get_attribute('placeholder')
    if actual_placeholder != expected_placeholder:
        driver.save_screenshot('screenshots/search_field_placeholder.png')
        driver.quit()
        fail(f'Expected placeholder text is "{expected_placeholder}", but actual was: "{actual_placeholder}"')
    driver.quit()

def test_search_case_sensitivity():
    driver = start_driver()
    login_as_test_user(driver)

    driver.find_element(By.NAME, 'q').send_keys('Unpublished Product')
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    expected_text = 'Products found : 1'
    actual_text = driver.find_element(By.TAG_NAME, 'p').text
    if actual_text != expected_text:
        driver.save_screenshot('screenshots/case_sensitivity_issue.png')
        driver.quit()
        fail(f'Expected text is "{expected_text}", but actual was: "{actual_text}"')
    driver.quit()