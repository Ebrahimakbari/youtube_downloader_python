from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests

quality = 0


def user_input():
    global quality
    url = input('enter youtube link: ')
    # url = 'https://www.youtube.com/watch?v=Q2zaO2C2vWk'
    quality = input('enter quality of video[720p,480p,360p,240p,144p]: ')
    # quality = '480p'
    q_dict = {
        '720p': 'btn22',
        '480p': 'btn135',
        '360p': 'btn18',
        '240p': 'btn133',
        '144p': 'btn160'
    }
    return url, q_dict[quality]


url, q = user_input()


def create_target_link(url):
    return url[:19] + 'pi' + url[19:]


def get_link(url, q):
    op = Options()
    op.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=op, service=Service(
        '../chromedriver.exe'))  # give your driver path
    driver.get(url)
    driver.maximize_window()
    # origin_page = driver.current_window_handle
    Wait = WebDriverWait(driver, 15)
    Wait.until(ec.element_to_be_clickable(
        (By.XPATH, f'//*[@id="{q}"]/button'))).click()
    # driver.switch_to.window(origin_page)
    row_link = Wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="btnOk"]/button/a')))
    link = row_link.get_attribute('href')
    driver.close()
    return link


def download_vid(link):
    with requests.get(link, stream=True) as r:
        total = int(r.headers.get('content-length'))
        print(f'video size == {total/(1024*1024)}')
        download = 0
        with open(f'{quality}.mp4', 'wb') as f:
            print('downloading...')
            for data in r.iter_content(1024):
                download += len(data)
                downloaded = int(100*download/total)
                print(f'\r[{'O'*downloaded}{' '*(100-downloaded)}]', end='')
                f.write(data)
    print('\ndownload completed!!!!')


download_vid(get_link(create_target_link(url), q))
