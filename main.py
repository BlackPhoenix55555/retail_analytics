import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.walmart.com/search?q=laptop"

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=145)
driver.get(URL)

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-item-id]")))

# Smart scrolling
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

products = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")

print(f"Found {len(products)} products")

with open("walmart_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])

    for product in products:
        # Name
        try:
            name = product.find_element(
                By.CSS_SELECTOR,
                "[data-automation-id='product-title']"
            ).text.strip()
        except:
            name = "N/A"

        # Price
        try:
            price = product.find_element(
                By.CSS_SELECTOR,
                "[data-automation-id='product-price']"
            ).text.strip()
        except:
            try:
                price = product.find_element(
                    By.CSS_SELECTOR,
                    "span[class*='price']"
                ).text.strip()
            except:
                price = "N/A"

        if name != "N/A":
            print(name, price)
            writer.writerow([name, price])

driver.quit()
print("Scraping Completed ✅")
