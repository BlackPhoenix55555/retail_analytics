import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.walmart.com/search?q=laptop"

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options,version_main=145)
driver.get(URL)

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-item-id]")))

# Controlled Smart Scrolling (Max 10 scrolls)
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

products = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
print(f"Found {len(products)} products")

with open("walmart_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price"])

    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR,"[data-automation-id='product-title']").text.strip()
        except:
            continue  # Skip if no product title

        try:
            price = product.find_element(By.CSS_SELECTOR,"[data-automation-id='product-price']").text.strip()
        except:
            price = "N/A"

        print(name, price)
        writer.writerow([name, price])

driver.quit()
print("Scraping Completed ✅")
