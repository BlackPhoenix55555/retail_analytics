import csv
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# -------- CONFIG --------
QUERY = "laptop"
BASE_URL = f"https://www.walmart.com/search?q={QUERY}&page={{}}"

# -------- BROWSER SETUP --------
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=145)
driver.set_page_load_timeout(60)

wait = WebDriverWait(driver, 35)

# -------- START CRAWLING --------
with open("walmart_crawled_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Product Name", "Price"])

    page = 1

    while True:

        print(f"\nCrawling Page {page}...")

        try:
            driver.get(BASE_URL.format(page))

            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-item-id]")
                )
            )

        except TimeoutException:
            print("⚠ Timeout or no more pages. Stopping crawler.")
            break

        # Scroll
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))

        products = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")

        # Stop if no products found
        if len(products) == 0:
            print("✅ No more products found. Reached last page.")
            break

        print(f"Found {len(products)} products on Page {page}")

        for product in products:
            try:
                name = product.find_element(
                    By.CSS_SELECTOR,
                    "[data-automation-id='product-title']"
                ).text.strip()
            except:
                continue

            try:
                price = product.find_element(
                    By.CSS_SELECTOR,
                    "[data-automation-id='product-price']"
                ).text.strip()
            except:
                price = "N/A"

            print(name, price)
            writer.writerow([page, name, price])

        page += 1
        time.sleep(random.uniform(5, 9))

driver.quit()
print("\nCrawling Completed Successfully ✅")
