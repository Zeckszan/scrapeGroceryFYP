from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
from browsermobproxy import Server
import time


CHROME_PATH = "C:\Program Files (x86)\chromedriver.exe"

def get_to_process(url,shared_results, selectors):
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

        time.sleep(4)
        # Close pop up
        try:
            poscode = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@class="cpk-input"]'))
            )
            poscode.send_keys("50450")
            time.sleep(5)

            verify_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="postcode-popup-inner"]/div[3]/div'))
            )
            verify_btn.click()
        except Exception as e:
            print("Error closing pop up ",e)
            pass

        try:
            # Locate all elemnets in the pagination element and extract total number of pages
            all_page_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//*[@id="shopify-section-collection_page"]/div[3]/nav/ul/li/a'))
            )

            last_page = all_page_elements[-2].text
            number_of_pages = int(last_page)
            print(f'Total number of pages: {last_page}')

            for page in range(number_of_pages):
                page_links.append(f'{url}?page={page + 1}')

            for link in page_links:
                print(link)
                driver.get(link)
                time.sleep(1)
                try:
                    poscode = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@class="cpk-input"]'))
                    )
                    poscode.send_keys("41200")
                    time.sleep(5)

                    verify_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="postcode-popup-inner"]/div[3]/div'))
                    )
                    verify_btn.click()
                except Exception as e:
                    print("Error closing pop up ")
                    pass

                product_names=driver.find_elements(By.CSS_SELECTOR, "a.cd.chp")
                product_prices=driver.find_elements(By.CSS_SELECTOR, '.price')

                for x in range(len(product_names)):
                    print(product_names[x].text)

                    try:
                        product_prices[x].find_element(By.CSS_SELECTOR, 'ins')
                        product_price = product_prices[x].find_element(By.CSS_SELECTOR, 'ins').text
                        print(product_prices[x].find_element(By.CSS_SELECTOR, 'ins').text)
                    except:
                        product_price = product_prices[x].text
                        print(product_prices[x].text)

                    shared_results.append({
                        'product_name': product_names[x].text.title(),
                        'price': product_price
                    })
                    print('=' * 45)
        except:
            print(f"[Error] Cannot extract product name.")
            pass

    except Exception as e:
        print(f"[Error] Exception in scrape_chunk: {e}")
    finally:
        driver.close()
        server.stop()

def start_scraping_vgw(url, url2, selectors):
    manager = multiprocessing.Manager()
    shared_results = manager.list()
    get_to_process(url, shared_results, selectors)
    get_to_process(url2, shared_results, selectors)
    return list(shared_results)
