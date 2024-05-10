from selenium import webdriver
import undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from random import randrange
import os


def simulate_user(url: str, products_count: int):
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    )
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = undetected_chromedriver.Chrome(options=options)
    list_with_items_info = []
    try:
        driver.get(url)
        counter = 0
        while counter != products_count:
            sleep(8)
            items = driver.find_elements(By.XPATH, "//div[@class='yi4']/a")

            for item in items[30:]:
                item.send_keys(Keys.CONTROL + Keys.RETURN)
                sleep(randrange(1, 2))
                driver.switch_to.window(driver.window_handles[-1])
                wait = WebDriverWait(driver, 30)
                wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='jp1'][1]")))
                sleep(randrange(2, 3))
                list_with_items_info.append(parse_info(driver.page_source))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                counter += 1
                if counter == products_count: break
                sleep(randrange(1, 2))

            driver.find_element(By.XPATH, "//a[@class='en4 b213-a0 b213-b6 b213-b1']").click()
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return list_with_items_info


def parse_info(html_document):
    dict_with_item_info = {}
    soup = BeautifulSoup(html_document, 'lxml')
    dict_with_item_info['name'] = soup.find('h1', class_='l0y tsHeadline550Medium').text.strip()
    if soup.find('span', class_='l4x xl4 l8'):
        encode_price = soup.find('span', class_='l4x xl4 l8').text
        dict_with_item_info['price'] = int(encode_price.replace('\u2009', '')[:-1])
    else:
        encode_price = soup.find('span', class_='x3l x4l x2l lx4').text
        dict_with_item_info['price'] = int(encode_price.replace('\u2009', '')[:-1])
    if soup.find('div', class_='wk3'):
        dict_with_item_info['description'] = soup.find('div', class_='wk3').text.replace('\xa0', '')
    else: dict_with_item_info['description'] = None
    dict_with_item_info['image_url'] = soup.find('div', class_='v8j jv9').find('img').get('src')
    if soup.find('div', class_='lm9 b13-a0'):
        dict_with_item_info['discount'] = int(soup.find('div', class_='lm9 b13-a0').text[1:-1])
    else: dict_with_item_info['discount'] = None
    return dict_with_item_info


parsing_url = 'https://www.ozon.ru/seller/1'