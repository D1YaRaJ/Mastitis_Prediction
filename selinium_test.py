import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def print_test_header(test_name):
    print(f"\n\033[1;34m=== {test_name.upper()} ===\033[0m")

def print_step(step):
    print(f"  \033[1;36m• {step}\033[0m")

def print_success():
    print("  \033[1;32m✓ PASSED\033[0m")

@pytest.fixture(scope="function")
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_homepage_load(browser):
    print_test_header("Homepage Load Test")
    print_step("Loading homepage")
    browser.get("http://localhost:5000")
    
    print_step("Checking page title")
    assert "Mastitis Prediction" in browser.title, \
        f"Expected 'Mastitis Prediction' in title, got: '{browser.title}'"
    
    print_step("Checking welcome message")
    assert "Welcome" in browser.page_source, \
        "Welcome message not found in page source"
    
    print_step("Verifying form elements")
    elements = {
        "Temperature Field": "temperature",
        "Hardness Dropdown": "hardness",
        "Pain Dropdown": "pain"
    }
    
    for name, elem_id in elements.items():
        print(f"    - Checking {name} (ID: {elem_id})")
        assert browser.find_element(By.ID, elem_id).is_displayed()
    
    print_success()

def test_prediction_flow(browser):
    print_test_header("Prediction Flow Test")
    browser.get("http://localhost:5000")
    
    print_step("Filling valid form data")
    test_data = {
        "temperature": ("38.5", "Temperature"),
        "hardness": ("3", "Udder Hardness"),
        "pain": ("2", "Pain Score"),
        "milk_visibility": ("1", "Milk Visibility"),
        "milk_color": ("2", "Milk Color")
    }
    
    for field, (value, name) in test_data.items():
        if field in ["hardness", "pain", "milk_visibility", "milk_color"]:
            print(f"    - Selecting {name}: {value}")
            Select(browser.find_element(By.ID, field)).select_by_value(value)
        else:
            print(f"    - Entering {name}: {value}")
            browser.find_element(By.ID, field).send_keys(value)
    
    print_step("Submitting form")
    browser.find_element(By.XPATH, "//button[contains(text(),'Predict')]").click()
    
    print_step("Verifying prediction result")
    result = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "result"))
    ).text
    assert "Mastitis" in result, f"Unexpected result: {result}"
    
    print_success()

def test_no_mastitis_prediction(browser):
    print_test_header("No Mastitis Prediction Test")
    
    # 1. Load the page
    print_step("Loading application page")
    browser.get("http://localhost:5000")
    
    # 2. Fill form with healthy parameters
    print_step("Filling form with cow data")
    healthy_data = {
        "temperature": ("38.0", "Normal Temperature"),  # Healthy range
        "hardness": ("0", "No Udder Hardness"),
        "pain": ("0", "No Pain"),
        "milk_visibility": ("0", "Normal Milk Yield"),
        "milk_color": ("0", "Normal Milk Color")
    }
    
    for field, (value, description) in healthy_data.items():
        if field in ["hardness", "pain", "milk_visibility", "milk_color"]:
            print(f"    - Selecting {description}: {value}")
            Select(browser.find_element(By.ID, field)).select_by_value(value)
        else:
            print(f"    - Entering {description}: {value}")
            browser.find_element(By.ID, field).send_keys(value)
    
    # 3. Submit form
    print_step("Submitting form")
    browser.find_element(By.XPATH, "//button[contains(text(),'Predict')]").click()
    
    # 4. Verify result
    print_step("Checking prediction result")
    result = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "result"))
        ).text.lower()  # Convert to lowercase for case-insensitive check
    assert "no mastitis" in result, f"Unexpected result: {result}"
    print_success()

def test_form_validation(browser):
    print_test_header("Form Validation Test")
    browser.get("http://localhost:5000")
    
    print_step("Testing invalid temperature (50.0)")
    browser.find_element(By.ID, "temperature").send_keys("50")
    browser.find_element(By.XPATH, "//button[contains(text(),'Predict')]").click()
    
    print_step("Checking error message")
    error = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "result"))
    ).text
    assert "Temperature must be" in error, f"Unexpected error: {error}"
    
    print_success()
    
def test_hardness_validation(browser):
    print_test_header("Udder Hardness Validation Test")
    browser.get("http://localhost:5000")
    
    # FIRST fill ALL required fields with valid values
    print_step("Filling base valid values")
    browser.find_element(By.ID, "temperature").send_keys("38.5")  # Valid temp
    Select(browser.find_element(By.ID, "pain")).select_by_value("0")  # No pain
    Select(browser.find_element(By.ID, "milk_visibility")).select_by_value("0")  # Normal milk
    Select(browser.find_element(By.ID, "milk_color")).select_by_value("0")  # Normal color
    
    # THEN test hardness values
    print_step("Testing hardness values")
    valid_values = ["0", "3", "5"]  # Min, middle, max valid values
    
    for value in valid_values:
        print(f"    - Selecting hardness: {value}")
        Select(browser.find_element(By.ID, "hardness")).select_by_value(value)
        browser.find_element(By.XPATH, "//button[contains(text(),'Predict')]").click()
        
        result = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((By.ID, "result"))
        ).text.lower()
        
        assert "invalid" not in result, f"Unexpected error for hardness {value}: {result}"
        assert "must be" not in result, f"Unexpected validation for hardness {value}: {result}"
        
        # Refresh and re-fill base values
        browser.refresh()
        browser.find_element(By.ID, "temperature").send_keys("38.5")
        Select(browser.find_element(By.ID, "pain")).select_by_value("0")
        Select(browser.find_element(By.ID, "milk_visibility")).select_by_value("0")
        Select(browser.find_element(By.ID, "milk_color")).select_by_value("0")
    
    print_success()