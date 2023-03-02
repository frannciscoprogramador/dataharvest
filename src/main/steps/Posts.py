import time
import urllib.request
from src.main.utils.Constants import GENERAL_WAITING_TIME, PAUSE_ANTI_BOT, GENERAL_EXPLICIT_WAIT_TIME
from src.main.config.WebDriver import WebDriver
from src.main.config.Logger import Logger
from src.main.steps.Download import Download
from src.main.config.SQL import SQL
from src.main.utils.Utils import increment_filename, create_folder_if_not_exists


class Posts:
    def __init__(self, web_driver: WebDriver, sql: SQL):
        self.logger = Logger('[           Posts           ]')
        self.web_driver = web_driver
        self.general_wait_time = GENERAL_WAITING_TIME
        self.general_explicit_wait_time = GENERAL_EXPLICIT_WAIT_TIME
        self.sql = sql
        self.download = Download(self.web_driver, self.sql)
        self.pause_anti_bot = PAUSE_ANTI_BOT

    def scroll_page(self):
        while True:
            last_height = self.web_driver.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self.web_driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

    def grid_href(self):
        hrefs = []
        try:
            divs = self.web_driver.all_by_css_selector('div._aabd._aa8k._aanf', 5)
            for div in divs:
                a = self.web_driver.execute_script_to_div("return arguments[0].querySelectorAll('a')", div)
                for enlace in a:
                    href = enlace.get_attribute('href')
                    hrefs.append(href)
            return hrefs
        except Exception as ex:
            self.logger.info(f"error grid_href: {ex}")

    def obtain_file(self, resources, profile):
        try:
            time.sleep(self.general_wait_time)

            img_script = self.web_driver.execute_script("return document.querySelector('div._aagv')")
            img = self.web_driver.execute_script_to_div("return arguments[0].querySelector('img[srcset*=\"1080w\"]')", img_script)

            video_div = self.web_driver.execute_script("return document.querySelector('div.x5yr21d video')")

            timer_file = self.web_driver.by_css_selector('time._a9ze._a9zf', self.general_wait_time)
            time_class = timer_file.get_attribute("title")

            path = f'{resources}/{profile}/posts/'
            create_folder_if_not_exists(path)
            name = increment_filename(f'{path}/{time_class}')

            if video_div:
                video_src = video_div.get_attribute('src')
                urllib.request.urlretrieve(video_src, name)
            elif img:
                src = img.get_attribute('src')
                urllib.request.urlretrieve(src, name)

        except Exception as ex:
            self.logger.info(f"error obtain_file: {ex}")

    def next_posts(self, resources, profile):
        try:
            self.obtain_file(resources, profile)
            time.sleep(self.general_wait_time)
            next_button = self.web_driver.by_css_selector('button._afxw._al46._al47', self.general_wait_time)
            while next_button:
                next_button = self.web_driver.by_css_selector('button._afxw._al46._al47', self.general_wait_time)
                if next_button:
                    time.sleep(self.general_wait_time)
                    next_button.click()
                    self.obtain_file(resources, profile)
                else:
                    break
        except Exception as ex:
            self.logger.info(f"error next_posts: {ex}")

    def posts(self, resources, profile):
        # self.scroll_page()
        hrefs = self.grid_href()
        if hrefs:
            for post in hrefs:
                self.web_driver.open(post)
                self.next_posts(resources, profile)
