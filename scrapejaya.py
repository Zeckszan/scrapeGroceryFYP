from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
import multiprocessing
import time


CHROME_PATH = "C:\Program Files (x86)\chromedriver.exe"

def get_to_process_jaya(url,shared_results,selectors):

    page_links = []

    server = Server(path="C:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat", options={'port': 8090})
    server.start()
    proxy = server.create_proxy()

    try:
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))  # Add this line to configure the proxy
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(CHROME_PATH, options=chrome_options)
        driver.maximize_window()
        driver.get(url)

        # Close Pop Up Window
        try:
            poscode = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="rbz-zipcode"]'))
            )
            poscode.send_keys("50450")
            poscode.send_keys(Keys.RETURN)

            verify_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="zipcode-input-submit-button"]'))
            )
            time.sleep(3)
            verify_btn.click()
        except:
            print(f"[Error] No pop up window.")
            pass

        # Locate all elemnets in the pagination element and extract total number of pages
        all_page_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//*[@id="shopify-section-collection-template"]/section/div[1]/div[2]/div/div/div/div[2]/div[3]/div/div/a'))
        )
        print("all page ele",all_page_elements)

        last_page = all_page_elements[-1].text
        number_of_pages = int(last_page)
        print(f'Total number of pages: {last_page}')

        for page in range(number_of_pages):
            page_links.append(f'{url}?page={page + 1}')

        for link in page_links:
            print(link)

            driver.get(link)

            # Close Pop Up Window
            try:
                poscode = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="rbz-zipcode"]'))
                )
                poscode.send_keys("50450")
                poscode.send_keys(Keys.RETURN)

                verify_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="zipcode-input-submit-button"]'))
                )
                time.sleep(2)
                verify_btn.click()
            except:
                print(f"No pop up window.")
                pass

            # Extract data
            product_names = driver.find_elements(By.CSS_SELECTOR, selectors.get("product_name"))
            product_prices = driver.find_elements(By.CSS_SELECTOR, selectors.get("price"))

            for x in range(len(product_names)):
                shared_results.append({
                    'product_name': product_names[x].text,
                    'price': product_prices[x].text
                })
                print(f'Product: {product_names[x].text}')
                print(f'Price: {product_prices[x].text}')
                print('=' * 45)

    except Exception as e:
        print(f"[Error] Exception in scrape_chunk: {e}")
    finally:
        driver.close()
        server.stop()


def start_scraping_jaya(url, url2, selectors):
    manager = multiprocessing.Manager()
    shared_results = manager.list()

    get_to_process_jaya(url,shared_results,selectors)
    get_to_process_jaya(url2, shared_results, selectors)

    return list(shared_results)



