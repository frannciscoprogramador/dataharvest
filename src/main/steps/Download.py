import time
from src.main.utils.Utils import increment_filename
import requests
from src.main.config.WebDriver import WebDriver
from src.main.config.Logger import Logger
from src.main.utils.Constants import GENERAL_WAITING_TIME, GENERAL_EXPLICIT_WAIT_TIME
from src.main.config.SQL import SQL


class Download:
    def __init__(self, web_driver: WebDriver, sql: SQL):
        self.logger = Logger('[          Download         ]')
        self.web_driver = web_driver
        self.general_wait_time = GENERAL_WAITING_TIME
        self.sql = sql

    def pause_store(self):
        play_button = self.web_driver.by_css_selector('svg._ab6-[aria-label]', self.general_wait_time)
        aria_label = play_button.get_attribute('aria-label')
        if aria_label == 'Pause':
            play_button.click()

    def download_img(self, path_file, profile):
        img = self.web_driver.by_css_selector('img._aa63._ac51', self.general_wait_time)
        if img:
            try:
                srcset = img.get_attribute('srcset')
                img_urls = srcset.split(', ')
                img_url_1080w = None
                for url in img_urls:
                    exists_download = self.sql.check_src_exists(url)
                    if not exists_download:
                        if '1080w' in url:
                            img_url_1080w = url.split(' ')[0]
                            break
                        if '720w' in url:
                            img_url_1080w = url.split(' ')[0]
                            break
                    self.logger.info('a download was prevented because it already exists')
                if img_url_1080w:
                    img_file = requests.get(img_url_1080w)
                    name = increment_filename(path_file)
                    open(f"{name}", "wb").write(img_file.content)
                    self.sql.insert_src(profile, img_url_1080w)
                    self.logger.info(f'an insert was generated for {profile} type img {img_url_1080w}')
            except Exception as e:
                self.logger.info(f"An error occurred while making the request to img: {e}")

    def download_video(self, path_file, profile):
        video_element = self.web_driver.find_element_by_xpath('//video', self.general_wait_time)
        exists_blob = False
        if video_element:
            src_url = video_element.get_attribute('src')
            exists_download = self.sql.check_src_exists(src_url)
            if not exists_download:
                try:
                    response = requests.get(src_url)
                    name = increment_filename(path_file)
                    with open(name, 'wb') as f:
                        f.write(response.content)
                        self.sql.insert_src(profile, src_url)
                        self.logger.info(f'download {src_url}')
                except Exception as e:
                    exists_blob = True
                    self.logger.info(f"An error occurred while making the request to video: {e}")
            self.logger.info('a download was prevented because it already exists')
        if exists_blob:
            actual = self.web_driver.current_url()
            self.web_driver.refresh()
            time.sleep(GENERAL_WAITING_TIME)
            btn_view_stories = self.web_driver.by_css_selector('button._acan._acap._acau._acav._aj1-',
                                                               GENERAL_EXPLICIT_WAIT_TIME)
            if btn_view_stories:
                btn_view_stories.click()
                self.pause_store()
            later = self.web_driver.current_url()
            if not actual == later:
                self.web_driver.open(actual)
            else:
                self.download_video(path_file, profile)
