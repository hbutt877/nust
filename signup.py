import random
from time import sleep, time
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#import undetected_chromedriver as uc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from captcha import solve



engine = create_engine('sqlite:///accounts.db', connect_args={'check_same_thread': False})

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

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

# {'x': 808, 'y': 166}
# {'x': 376, 'y': 443}


def get_chromedriver():
    # driver = uc.Chrome()
    #chrome_options = uc.ChromeOptions()
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_extension('proxy_auth_plugin.zip')
    # chrome_options.add_extension('proxyrack.zip')
    #chrome_options.add_extension('./ext.crx')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_prefs = {}
    #chrome_options.experimental_options["prefs"] = chrome_prefs
    #chrome_prefs["profile.default_content_settings"] = {"images": 2}
    #chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    #driver = uc.Chrome(options=chrome_options)
    # if not server:
    #     driver.set_window_size(1285, 788)
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    return driver


emails = {}


def main():
    try:
        if server:
            display = Display(visible=False, size=(2600, 800))
            display.start()
        sent = False
        driver = get_chromedriver()
        driver.get('https://10minemail.net/')
        email = driver.find_elements_by_xpath('//h3[contains(text(),"@")]')
        if email:
            email = email[0].text
        else:
            print('error email')
            return
        if '@' not in email:
            print('ERROR NO EMAIL', email)
            return
        print(email)
        if email in emails:
            print('duplicate')
            return
        else:
            emails[email] = True

        email_window = driver.current_window_handle
        driver.execute_script('''window.open("","_blank");''')
        coin_window = driver.window_handles[1]
        driver.switch_to.window(coin_window)

        print('coinmarket')

        driver.get('https://coinmarketcap.com/')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sign up"]'))).click()
        print('result wait')
        result = solve()
        print(result)
        if not(result and result != 'error'):
            print('error 2captcha')
            return None
        code = result['code']
        ##___grecaptcha_cfg.clients[0].l.l.callback
        sleep(1)
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(email)
        driver.find_element_by_xpath('//input[@type="password"]').send_keys('Allah786$\n')
        sleep(3)
        try:
            driver.execute_script(
                'document.getElementById("g-recaptcha-response").innerHTML = "%s"'
                % code
            )
        except:
            return None
        _ = 0
        while 1:
            driver.execute_script(f'___grecaptcha_cfg.clients[0].l.l.callback("{code}")')
            sleep(3)
            if len(driver.find_elements_by_xpath('//*[contains(text(),"sent an email")]')) > 0:
                sent = True
                break
            print('waiting')
            _ += 1
            if _ > 30:
                print('login error too much time loading')
                driver.save_screenshot('new.png')
                return
        if not sent:
            print('no sent mail')
            return
        driver.switch_to.window(email_window)
        print('waiting for email')
        _ = 0
        verify_mail = None
        for i in range(12):
            try:
                if _ > 12:
                    print('no mail a minute')
                    driver.save_screenshot('error.png')
                    return
                _ += 1
                verify_mail = driver.find_element_by_xpath('//*[text()="Verify your CoinMarketCap account"]')
                break
            except Exception as e:
                sleep(5)
        if verify_mail:
            driver.execute_script("arguments[0].click();", verify_mail)
            print('email opened')
        else:
            print('error in verify email')
            driver.save_screenshot(f'ee{random.randint(5,20)}.png')
            return
        sleep(2)
        while 1:
            try:
                verify_mail_link = driver.find_element_by_xpath('//a[text()="Click here to verify account"]')
                break
            except:
                sleep(2)
        if verify_mail_link:
            l = verify_mail_link.get_attribute('href')
            driver.get(l)
            sleep(1)
            print('v__')
            user = User(email=email, password='Allah786$')
            session.add(user)
            session.commit()
            print(email, ' verified ......................')

    except Exception as e:
        print(e)
        driver.save_screenshot(f'{random.randint(5,20)}.png')
    finally:
        if server:
            display.stop()
        try:
            driver.quit()
        except:
            pass
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=30) as ex:
        for i in range(30):
            ex.submit(main)
