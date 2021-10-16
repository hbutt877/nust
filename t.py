import random
from time import sleep, time
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from pyvirtualdisplay import Display
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from fake_useragent import UserAgent

PROXY = '95.216.10.237:5008'

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(f'--proxy-server={PROXY}')
#    service = Service('./chromedriver')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    return driver

def get_chromedriver_uc():
    import undetected_chromedriver as uc
    chrome_options = uc.ChromeOptions()
    #chrome_options.headless = True
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--proxy-server={PROXY}')
    driver = uc.Chrome(options=chrome_options)
    return driver


coins = ['centric swap']

def main():
    try:
        display = None
        display = Display(visible=False, size=(2600, 800))
        display.start()
        driver = get_chromedriver()
        for coin in coins:
            driver.get('https://coinmarketcap.com/')
            print(1)
            search_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Search"]')))
            search_button.click()
            sleep(random.randint(1, 3))
            print(2)
            search = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@spellcheck="false"]')))
            search.send_keys(coin)
            sleep(random.randint(2, 5))
            search.send_keys('\n')
            print(3)
            driver.execute_script(f'window.scrollBy(0,2000);')
            sleep(random.randint(3, 5))
            if driver.find_elements_by_xpath('//button[contains(text(),"Good")]'):
                good = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Good")]')))
                good.click()
#                sleep(random.randint(1, 3))
                print('GOOD DONE ')
            else:
                print('GOOD NOT DONE ')
            driver.execute_script(f'window.scrollBy(0,{random.randint(0,3000)});')
            sleep(random.randint(1, 4))
        print('SEARCH DONE ')
        driver.save_screenshot('done.png')

    except Exception as e:
        print('errorrrrr', e)
        driver.save_screenshot('eroooooors.png')
    finally:
        try:
            driver.delete_all_cookies()
            driver.quit()
            display.stop()
        except:
            pass






if __name__=='__main__':
#    main()
#    exit()
    start_time = time()
    with ThreadPoolExecutor(max_workers=50) as ex:
        for i in range(50):
            ex.submit(main)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")
