import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

BASE_URL = "http://localhost:5173"

def login(driver, wait):
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.presence_of_element_located((By.ID, "username-field"))).send_keys("testsubject")
    driver.find_element(By.ID, "password-field").send_keys("Sifra123", Keys.RETURN)
    wait.until(EC.url_to_be(f"{BASE_URL}/"))

@pytest.mark.e2e
def test_add_to_cart_flow(driver):
    wait = WebDriverWait(driver, 10)
    login(driver, wait)

    product_card = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/article[4]')))
    product_card.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/products/24"))

    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-cta")))
    add_to_cart_btn.click()

    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == 'Success: Added 1 unit(s) of "Logitech MX Master 3S" to your cart!'
    alert.accept()

@pytest.mark.e2e
def test_remove_from_cart(driver):
    wait = WebDriverWait(driver, 10)
    login(driver, wait)

    cart_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-cart-icon-btn")))
    cart_icon.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/cart"))

    remove_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart-item-remove-btn")))
    remove_btn.click()

    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, "return-shop-btn"))).is_displayed()

@pytest.mark.e2e
def test_checkout_flow(driver):
    wait = WebDriverWait(driver, 10)
    login(driver, wait)

    product_card = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/article[4]')))
    product_card.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/products/24"))

    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-cta")))
    add_to_cart_btn.click()

    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    cart_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-cart-icon-btn")))
    cart_icon.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/cart"))

    checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-cta-btn")))
    checkout_btn.click()

    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Success" in alert.text
    alert.accept()

@pytest.mark.e2e
def test_ai_product_generation(driver):
    wait = WebDriverWait(driver, 10)
    login(driver, wait)

    avatar_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "profile-avatar-btn")))
    avatar_btn.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/dashboard"))

    create_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "create-product-trigger-btn")))
    create_btn.click()

    wait.until(EC.url_to_be(f"{BASE_URL}/create-product"))

    ai_trigger_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ai-action-trigger-btn")))
    ai_trigger_btn.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-subtitle")))

    textarea = driver.find_element(By.CLASS_NAME, "modal-prompt-textarea")
    textarea.send_keys(
        'Selling my lightly used MacBook Pro 14-inch. It is in excellent, fully functional condition with '
        'no scratches, dents, or screen issues. The laptop has been very well cared for and kept in a '
        'protective sleeve. Apple MacBook Pro 14" M3 Pro 18GB RAM, 512GB SSD, Space Black .'
    )

    generate_btn = driver.find_element(By.CLASS_NAME, "modal-generate-btn")
    generate_btn.click()

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-subtitle")))

    select_element = wait.until(EC.presence_of_element_located((By.ID, "prod-subcat")))
    select = Select(select_element)
    assert select.first_selected_option.get_attribute("value") == "2"