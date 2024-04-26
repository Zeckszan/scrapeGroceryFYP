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

def get_to_process(url,shared_results, selectors):
    # first iterate to get all item to be processed
    # BrowserMob Proxy setup

    items = []

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

        #infinite scrolling down until max
        try:
            time.sleep(5)
            prev_height = driver.execute_script('return document.body.scrollHeight')
            while True:
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(10)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == prev_height:
                    break
                prev_height = new_height

        except Exception as e:
            print('unable to scroll',e)
            pass

        product_names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.ID, selectors.get("product_name")))
        )
        product_prices = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, selectors.get("price")))
        )
        #product_names = driver.find_elements(By.ID, selectors.get("product_name"))
        #product_prices = driver.find_elements(By.CLASS_NAME, selectors.get("price"))

        for x in range(len(product_names)):
            #print(x.get_attribute("innerText"))
            print(product_names[x].text)
            print(product_prices[x].text)
            shared_results.append({
                'product_name': product_names[x].text.title(),
                'price': 'RM'+product_prices[x].text
            })
            print('=' * 45)

        print("product name ",product_names)
        print("product price ", product_prices)

    except Exception as e:
        print(f"[Error] Exception in scrape_chunk: {e}")
    finally:
        driver.close()
        server.stop()
    return items


def start_scraping_lotus(url,url2, selectors):

    manager = multiprocessing.Manager()
    shared_results = manager.list()

    get_to_process(url, shared_results, selectors)
    get_to_process(url2, shared_results, selectors)

    return list(shared_results)
