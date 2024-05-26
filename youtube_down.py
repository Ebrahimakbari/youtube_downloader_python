from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests


def user_input():
    # url = input('enter youtube link: ')
    url = 'https://www.youtube.com/watch?v=54PilOtIrAM'
    # quality = input('enter quality of video[auto,1080p,720p,480p,240p]: ')
    quality = '480p'
    q_dict = {
        'auto': '1',
        '1080p': '2',
        '720p': '3',
        '480p': '4',
        '240p': '5'
    }
    return url, q_dict[quality]


url, q = user_input()


def create_target_link(url):
    return url[:19] + 'pp' + url[19:]


def get_link(url, q):
    op = Options()
    op.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=op, service=Service(
        '../chromedriver.exe'))  # give your driver path
    driver.get(url)
    driver.maximize_window()
    origin_page = driver.current_window_handle
    Wait = WebDriverWait(driver, 10)
    Wait.until(ec.element_to_be_clickable(
        (By.XPATH, f'//*[@id="mp4"]/table/tbody/tr[{q}]/td[3]/button'))).click()
    driver.switch_to.window(origin_page)
    row_link = Wait.until(ec.element_to_be_clickable(
        (By.XPATH, '//*[@id="process-result"]/div/a')))
    link = row_link.get_attribute('href')
    driver.close()
    return link


def download_vid(link):
    with requests.get(link, stream=True) as r:
        total = int(r.headers.get('content-length'))
        print(f'video size == {total}')
        download = 0
        with open(f'{q}.mp4', 'wb') as f:
            print('downloading...')
            for data in r.iter_content(4096):
                download += len(data)
                downloaded = int(100*download/total)
                print(f'\r[{'='*downloaded}{' '*(100-downloaded)}]', end='')
                f.write(data)


download_vid(get_link(create_target_link(url), q))
