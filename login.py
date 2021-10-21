import random
from time import sleep
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from captcha import solve



engine = create_engine('sqlite:///accounts3.db', connect_args={'check_same_thread': False})

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    orakuru = Column(Boolean)
    waultswap = Column(Boolean)
    centric_swap = Column(Boolean)
    def __repr__(self):
        return f'User {self.email}'


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
print(session.query(User).count())
server = True
if server:
    from pyvirtualdisplay import Display

# PROXY = '95.216.10.237:5008'
# PROXY = '209.205.212.35:444'


coins = ['centric swap']

def get_chromedriver():
    # driver = uc.Chrome()
    # chrome_options = uc.ChromeOptions()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)


    # chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_extension('nick_proxy.zip')
    # chrome_options.add_extension('obaid_proxy.zip')
    # chrome_options.add_extension('./ext.crx')
    # chrome_prefs = {}
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    # driver = uc.Chrome(options=chrome_options)
    # if not server:
    #     driver.set_window_size(1285, 788)
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    return driver


def main(email):
    try:
        logged_in = False
        if server:
            display = Display(visible=False, size=(2600, 800))
            display.start()
        driver = get_chromedriver()
        driver.get('https://coinmarketcap.com/')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Log In"]'))).click()
        # user = session.query(User).first()
        print('result wait ' + email)
        result = solve()
        # print(result)
        if not(result and result != 'error'):
            print('error 2captcha')
            return
        code = result['code']
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(email)
        driver.find_element_by_xpath('//input[@type="password"]').send_keys('Allah786$\n')
        sleep(3)
        driver.execute_script(
            'document.getElementById("g-recaptcha-response").innerHTML = "%s"'
            % code
        )

        _ = 0
        while 1:
            driver.execute_script(f'___grecaptcha_cfg.clients[0].B.B.callback("{code}")')
            sleep(3)
            avatar = driver.find_elements_by_xpath('//div[@class="avatar-img "]')
            if avatar:
                logged_in = True
                break
            print('waiting')
            _ += 1
            if _ > 10:
                print('login error too much time loading ' + email)
                driver.save_screenshot('new.png')
                return

        if logged_in:
            print('logged in')
            i = 0
            errors = 0
            while i < len(coins):
                try:
                    if errors > 1:
                        print('ERROR STOPING ' + email)
                        errors = 0
                        i += 1
                        continue
                    user = session.query(User).filter_by(email=email).first()
                    search_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[text()="Search"]')))
                    search_button.click()
                    sleep(random.randint(1, 3))
                    search = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@spellcheck="false"]')))
                    search.send_keys(coins[i])
                    sleep(random.randint(2, 5))
                    search.send_keys('\n')
                    sleep(random.randint(3, 4))
                    print('SEARCH DONE ' + email)
                    if not driver.find_elements_by_xpath('//span[@class="icon-Star-Filled"]/..'):
                        star = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[@class="icon-Star"]/..')))
                        star.click()
                        sleep(random.randint(1, 3))
                        print('STAR DONE ' + email)
                    else:
                        print('STAR NOT DONE ' + email)
#                        driver.save_screenshot('star.png')
                    driver.execute_script(f'window.scrollBy(0,2000);')
                    sleep(random.randint(2, 4))
                    if driver.find_elements_by_xpath('//button[contains(text(),"Good")]'):
                        good = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Good")]')))
                        good.click()
                        sleep(random.randint(1, 3))
                        print('GOOD DONE ' + email)
                    else:
                        print('GOOD NOT DONE ' + email)
#                        driver.save_screenshot('good.png')

                    if coins[i] == 'centric swap':
                        user.centric_swap = True
#                    elif coins[i] == 'orakuru':
#                        user.orakuru = True
                    else:
                        print('WRONG COIN STOPPPPPPPP')
                    session.commit()
                    i += 1
                    driver.get('https://coinmarketcap.com/')
                except Exception as e:
                    print('error occured ', e)
                    errors += 1
        else:
            print('ERROR not logged in')
            return
    except Exception as e:
        print(e)
    finally:
        if server:
            display.stop()
        try:
            driver.quit()
        except:
            pass

if __name__ == '__main__':
    u = session.query(User).filter_by(centric_swap=None).all()
#    main(u[0].email)
#    exit()
    random.shuffle(u)
    with ThreadPoolExecutor(max_workers=20) as ex:
        for i in u[:20]:
            ex.submit(main, i.email)
