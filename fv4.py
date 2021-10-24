import random
from time import sleep, time
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from pyvirtualdisplay import Display
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from fake_useragent import UserAgent

#ur = open("url.txt")
#link_st = ur.read()
#link = link_st.strip()
link = 'https://www.dextools.io/app/polygon/pair-explorer/0x3885503aef5e929fcb7035fbdca87239651c8154'
coin_name = 'kogecoin'
print(link)
#namee = open("coin.txt")
#link_st = namee.read()
#coin_name = link_st.strip()
print(coin_name)
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




def main():
    display = None
    display = Display(visible=False, size=(1200, 800))
    display.start()
    driver = get_chromedriver()
    main_window = driver.current_window_handle
    share = False
    top = True
    star = True
    trade = True
    for i in range(1, 2):
        try:
            driver.execute_script('''window.open("","_blank");''')
            new_window = driver.window_handles[i]
            driver.switch_to.window(new_window)
            driver.get('https://www.beautifyconverter.com/auto-refresh-page.php')
            el = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@name="url"]')))
            el.clear()
            el.send_keys(link)
            c = driver.find_element(By.XPATH,'//input[@id="startButton"]')
            driver.execute_script("arguments[0].click();", c)
        except Exception as e:
            print('refresher errorrrrr', e)
    print('refresher done')
    driver.switch_to.window(main_window)
    starred = False
    try:
        for i in range(5):
            try:
                driver.get(link)
                search_bar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input')))
                search_bar.clear()
                search_bar.send_keys(coin_name)
                link_el = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//li[@class="item ng-star-inserted"]')))
                if 'Sponsored' in link_el.text:
                    link_el = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '(//li[@class="item ng-star-inserted"])[2]')))
            except:
                link_el = None
            if link_el:
                link_el.click()
            else:
                driver.get(link)

            li_element0 = None
            try:
                # driver.get(link)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//li[contains(@class,"pair-price text")]')))
                sleep(random.randint(2, 4))
            except Exception as e:
                pass

            if top:
                try:
                    bsc = driver.find_elements(By.XPATH, '//div[contains(@class,"mt-2 d-inline-block align-bottom")]/a')
                    for button in bsc[:-1]:
                        button.click()
                        new_window = driver.window_handles[-1]
                        driver.switch_to.window(new_window)
                        sleep(random.randint(2, 4))
                        driver.close()
                        driver.switch_to.window(main_window)
                    print('bsc done')
                except Exception as e:
                    print(e, ' bsc')
                    # break

            if trade:
                try:
                    try:
                        info = driver.find_element(By.XPATH, '//button[text()="Info "]')
                        info.click()
                        sleep(1)
                    except:
                        pass
                    try:
                        trade = driver.find_element(By.XPATH,'//button[text()="Buy/Sell "]')
                        trade.click()
                    except:
                        pass
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Or try")]'))).click()
                    sleep(1)
                    new_window = driver.window_handles[-1]
                    driver.switch_to.window(new_window)
                    sleep(random.randint(1,3))
                    driver.close()
                    driver.switch_to.window(main_window)
                    print('trade done')
                except Exception as e:
                    print(e, 'trade')
                    break

            if share:
                try:
                    for i in range(6):
                        sleep(1)
                        li_element0 = driver.find_element(By.CLASS_NAME,"token-info-list").find_element(By.TAG_NAME,"li")
                        if li_element0:
                            break
                    share_button = li_element0.find_elements(By.TAG_NAME,"button")[1]
                    share_button.click()
                    sleep(random.randint(1,4))
                    model_content = driver.find_element(By.CLASS_NAME,"modal-content")
                    # ______________________________________ looping over each social site
                    try:
                        social_link = model_content.find_elements(By.TAG_NAME,"a")
                        random.shuffle(social_link)
                        for _ in social_link:
                            try:
                                driver.execute_script("arguments[0].click();", _)
                                sleep(random.randint(2,4))
                                new_window = driver.window_handles[-1]
                                driver.switch_to.window(new_window)
                                driver.close()
                                driver.switch_to.window(main_window)
                            except Exception as e:
                                pass
                    except Exception as e:
                        print("Problem in Getting social link", e)
                    # _______________________________________________________ Close model window
                    try:
                        if model_content:
                            close_model = model_content.find_element(By.CLASS_NAME,"modal-footer").find_element(By.TAG_NAME,"button")
                            driver.execute_script("arguments[0].click();", close_model)
                            print('share done')
                    except Exception as e:
                        print("Problem in closing model", e)
                except Exception as e:
                    print(e, ' share')
                    break
            if star:
                try:
                    if not starred:
                        star_button = driver.find_element(By.XPATH,'//button[starts-with(@class,"btn btn-success")]')
                        star_button.click()
                        sleep(random.randint(1,2))
                        starred = True
                        print('star done')
                    # star_button = driver.find_element(By.XPATH,'//button[starts-with(@class,"btn btn-secondary")]')
                    # star_button.click()
                    # sleep(random.randint(1,2))
                except Exception as e:
                    print(e,' star')

    except Exception as e:
        print(e,'closing erroorr')
    finally:
        try:
            driver.delete_all_cookies()
            driver.quit()
            if display:
                display.stop()
            print('closed')
        except:
            if display:
                display.stop()
            print('error in error')






if __name__=='__main__':
#    main()
#    exit()
    #start_time = time()
    with ThreadPoolExecutor(max_workers=50) as ex:
        while 1:
            ex.submit(main)
    #end_time = time()
    #elapsed_time = end_time - start_time
    #print(f"Elapsed run time: {elapsed_time} seconds")
