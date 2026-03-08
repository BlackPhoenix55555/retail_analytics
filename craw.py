import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.walmart.com/search?q=laptop&page={}"

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options, version_main=145)
wait = WebDriverWait(driver, 20)

with open("walmart_crawled_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Product Name", "Price"])

    # Crawl first 5 pages (you can increase)
    for page in range(1, 6):

        print(f"\nCrawling Page {page}...")
        driver.get(BASE_URL.format(page))

        # Wait until products load
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-item-id]")
            )
        )

        # Small scroll to trigger lazy loading
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        products = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
        print(f"Found {len(products)} products on page {page}")

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

driver.quit()
print("\nCrawling Completed ✅")
