import time
import random
import json
import boto3
from botocore.exceptions import ClientError
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------- CONFIG --------
QUERY = "laptop"
BASE_URL = f"https://www.walmart.com/search?q={QUERY}&page={{}}"
S3_BUCKET = "walmart-raw-tanmay"   # Your S3 bucket
MAX_RETRIES = 3                     # Retry failed page loads
SCROLL_TIMES = 2                    # Scrolls per page

# -------- AWS S3 SETUP --------
s3_client = boto3.client("s3")

def upload_to_s3(data, key):
    """Upload JSON object directly to S3"""
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        print(f"✅ Uploaded: {key}")
    except ClientError as e:
        print(f"❌ Upload failed: {e}")

# -------- BROWSER SETUP --------
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, version_main=145)
driver.set_page_load_timeout(40)
wait = WebDriverWait(driver, 35)

# -------- CRAWLING LOOP --------
page = 1
while True:
    print(f"\nCrawling Page {page}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            driver.get(BASE_URL.format(page))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-item-id]")))
            break  # Page loaded successfully
        except Exception as e:
            print(f"⚠ Attempt {attempt} failed for Page {page}: {e}")
            time.sleep(random.uniform(5, 10))
    else:
        print(f"❌ Failed to load Page {page} after {MAX_RETRIES} attempts. Stopping crawl.")
        break

    # Human-like scrolling
    for _ in range(SCROLL_TIMES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))

    products_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-item-id]")
    if not products_elements:
        print("🚫 No more products found. Crawling finished.")
        break

    products_data = []
    for prod in products_elements:
        try:
            name = prod.find_element(By.CSS_SELECTOR, "[data-automation-id='product-title']").text.strip()
        except:
            continue
        try:
            price = prod.find_element(By.CSS_SELECTOR, "[data-automation-id='product-price']").text.strip()
        except:
            price = "N/A"

        product_obj = {
            "page": page,
            "name": name,
            "price": price
        }
        products_data.append(product_obj)

    # Upload page products to S3
    if products_data:
        key = f"page_{page}_products.json"
        upload_to_s3(products_data, key)

    print(f"Found {len(products_data)} products on Page {page}")
    page += 1

    # Random delay before next page
    time.sleep(random.uniform(4, 7))

driver.quit()
print("\nCrawling Completed Successfully ✅")
