import random
from time import sleep, time
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
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
    chrome_options = uc.ChromeOptions()
    #    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_extension('proxy_auth_plugin.zip')
    # chrome_options.add_extension('proxyrack.zip')
    chrome_options.add_extension('./ext.crx')
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = uc.Chrome(options=chrome_options)
    if not server:
        driver.set_window_size(1285, 788)
    #    driver = webdriver.Chrome(executable_path='./newnick/chromedriver', options=chrome_options)
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
        sleep(3)
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(email)
        driver.find_element_by_xpath('//input[@type="password"]').send_keys('Allah786$\n')

        _ = 0
        while len(
                driver.find_elements_by_xpath('//iframe[@title="recaptcha challenge" and contains(@style,"px")]')) == 0:
            if len(driver.find_elements_by_xpath('//*[contains(text(),"sent an email")]')) > 0:
                sent = True
                break
            print('waiting')
            sleep(2)
            _ += 1
            if _ > 30:
                print('login error too much time loading')
                driver.save_screenshot('new.png')
                return

        action = webdriver.ActionChains(driver)
        close_button = driver.find_element_by_xpath('//*[contains(@class,"close-button")]')
        action.move_to_element(close_button)
        action.perform()

        if not sent:
            sleep(2)
            action.move_by_offset(-304, 570)
            action.perform()
            action.click()
            action.move_to_element(close_button)
            action.perform()
            c = 0
            error_count = 0
            while 1:
                try:
                    sleep(1)
                    if c > 7:
                        print('c')
                        break
                    if error_count > 1:
                        print('error count')
                        break

                    if len(driver.find_elements_by_xpath(
                            '//iframe[@title="recaptcha challenge" and contains(@style,"px")]')) == 0 \
                            and len(driver.find_elements_by_xpath('//button[contains(text(),"Logging")]')) > 0:
                        print('c += 2')
                        c += 2
                        continue

                    error_text = driver.find_elements_by_xpath('//div[@class="sc-1htht4q-3 kHSKLo last"]/div')
                    if len(error_text) > 2:
                        try:
                            driver.find_element_by_xpath('//input[@type="password"]').send_keys('\n')
                            while len(driver.find_elements_by_xpath(
                                    '//iframe[@title="recaptcha challenge" and contains(@style,"px")]')) == 0:
                                print('waiting 2')
                                sleep(2)
                        except:
                            pass
                        error_count += 1
                        print('red error text visible')
                        sleep(3)
                        action.move_by_offset(-235, 532)
                        action.perform()
                        action.click()
                        action.move_to_element(close_button)
                        action.perform()
                        c = 0
                        continue

                    t = driver.find_elements_by_xpath('//*[contains(text(),"sent an email")]')
                    if not t:
                        print('not t')
                        driver.save_screenshot('3.png')
                        action.move_by_offset(-235, 532)
                        action.perform()
                        action.click()
                        action.move_to_element(close_button)
                        action.perform()
                        c += 1
                    else:
                        sent = True
                        break
                except:
                    print('error.....')
                    return
        else:
            print('Email Sent')
        print('email sent ', sent)
        if not sent:
            print('no sent mail')
            return
        driver.switch_to.window(email_window)
        print('waiting for email')
        _ = 0
        while 1:
            try:
                if _ > 15:
                    print('no mail a minute')
                    return
                _ += 1
                verify_mail = driver.find_element_by_xpath('//*[text()="Verify your CoinMarketCap account"]')
                break
            except:
                sleep(4)
        if verify_mail:
            driver.execute_script("arguments[0].click();", verify_mail)
            print('email opened')
        else:
            print('error in verify email')
            return
        sleep(2)
        # iframe = driver.find_element_by_xpath('//iframe[@class="w-100 border-0"]')
        # driver.switch_to.frame(iframe)
        while 1:
            try:
                verify_mail_link = driver.find_element_by_xpath('//a[text()="Click here to verify account"]')
                break
            except:
                sleep(2)
        if verify_mail_link:
            #        driver.execute_script("arguments[0].click();", verify_mail_link)
            l = verify_mail_link.get_attribute('href')
            # driver.switch_to.default_content()
            driver.get(l)
            sleep(1)
            print('v__')
            user = User(email=email, password='Allah786$')
            session.add(user)
            session.commit()
            print(email, ' verified ......................')

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
    with ThreadPoolExecutor(max_workers=50) as ex:
        for i in range(50):
            ex.submit(main)
