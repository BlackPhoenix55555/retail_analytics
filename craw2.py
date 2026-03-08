import csv
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------- CONFIG --------
QUERY = "laptop"
MAX_PAGES = 14
BASE_URL = f"https://www.walmart.com/search?q={QUERY}&page={{}}"

# -------- BROWSER SETUP --------
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=145)
driver.set_page_load_timeout(40)

wait = WebDriverWait(driver, 35)

# -------- START CRAWLING --------
with open("walmart_crawled_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Product Name", "Price"])

    for page in range(1, MAX_PAGES + 1):

        print(f"\nCrawling Page {page}...")

        # Load page safely
        try:
            driver.get(BASE_URL.format(page))
        except:
            print(f"⚠ Timeout loading Page {page}, skipping...")
            continue

        # Wait for products
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-item-id]")
                )
            )
        except:
            print(f"⚠ No products found on Page {page}, skipping...")
            continue

        # Human-like scrolling
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))

        products = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
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

        # Random delay before next page
        time.sleep(random.uniform(4, 7))

driver.quit()
print("\nCrawling Completed Successfully ✅")
