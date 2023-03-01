import time
from src.main.utils.Utils import create_folder_if_not_exists
from src.main.utils.Constants import STORES, DIV_NAME_STORE, GENERAL_WAITING_TIME, STORES_TIMEOUT, NEXT_STORIES_BUTTON, \
    PAUSE_ANTI_BOT, GENERAL_EXPLICIT_WAIT_TIME
from src.main.config.WebDriver import WebDriver
from src.main.config.Logger import Logger
from src.main.steps.Download import Download
from src.main.config.SQL import SQL


class Stories:
    def __init__(self, web_driver: WebDriver, sql: SQL):
        self.logger = Logger('[          Stories          ]')
        self.web_driver = web_driver
        self.general_wait_time = GENERAL_WAITING_TIME
        self.stores_timeout = STORES_TIMEOUT
        self.div_storage_name = DIV_NAME_STORE
        self.stores = STORES
        self.sql = sql
        self.download = Download(self.web_driver, self.sql)
        self.pause_anti_bot = PAUSE_ANTI_BOT

    def pause_store(self):
        play_button = self.web_driver.by_css_selector('svg._ab6-[aria-label]', self.general_wait_time)
        aria_label = play_button.get_attribute('aria-label')
        if aria_label == 'Pause':
            play_button.click()

    def press_next_store_button(self):
        button = self.web_driver.by_css_selector('button._ac0d', NEXT_STORIES_BUTTON)
        if button:
            return button
        else:
            return False

    def get_src_for_download(self, path_file, profile):
        video = self.web_driver.by_css_selector('video.x1lliihq.x5yr21d.xh8yej3', self.general_wait_time)
        if video:
            self.download.download_video(path_file, profile)
        else:
            self.download.download_img(path_file, profile)

    def system_pause(self):
        time.sleep(self.pause_anti_bot)

    def first_featured_stores(self):
        first_stories = self.web_driver.all_by_css_selector('span.x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft',
                                                            GENERAL_EXPLICIT_WAIT_TIME)
        spans_name = [name.text for name in first_stories]
        first_value = spans_name[0]
        script = f"img[alt='{first_value}\\'s profile picture']"
        button_first_stories = self.web_driver.by_css_selector(script, GENERAL_EXPLICIT_WAIT_TIME)
        if button_first_stories:
            return script
        else:
            return False

    def name_file(self, path: str):
        timer_file = self.web_driver.by_css_selector('time._ac0t', self.general_wait_time)
        name_file = timer_file.get_attribute("title")
        path_file = f'{path}{name_file}'
        return path_file

    def len_inside_stories(self):
        inside_stories = self.web_driver.all_by_css_selector('div._ac3n', self.general_wait_time)
        len_inside_stories = len(inside_stories)
        return len_inside_stories

    def obtain_data_and_download(self, profile, resources):
        name_store = self.web_driver.by_css_selector(self.div_storage_name, self.stores_timeout)
        if name_store and name_store.text == profile:
            self.logger.info(f'the story has a name: {name_store.text}')
            path = f'{resources}/{profile}/{self.stores}/'
        else:
            self.logger.info(f'the story has a name: {name_store.text}')
            path = f'{resources}/{profile}/{self.stores}/{name_store.text}/'
        create_folder_if_not_exists(path)
        path_file = self.name_file(path)
        self.get_src_for_download(path_file, profile)

    def access_store(self, resources: str, profile: str, div_store: str):
        stores = self.web_driver.by_css_selector(div_store, self.stores_timeout)
        featured_stories = self.web_driver.by_all_css_selector('span.x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft', self.general_wait_time)
        len_featured_stories = 1
        if stores:
            stores.click()
            self.pause_store()
            btn_next_stories = self.press_next_store_button()
            if btn_next_stories:
                if featured_stories:
                    len_featured_stories = len(featured_stories)
                for h in range(len_featured_stories):
                    len_inside_stories = self.len_inside_stories()
                    for j in range(len_inside_stories):
                        self.obtain_data_and_download(profile, resources)
                        btn_next_stories = self.press_next_store_button()
                        if btn_next_stories:
                            btn_next_stories.click()
                            self.pause_store()
                            self.logger.info(f'count stories: {j}/{len_inside_stories}')
            else:
                path = f'{resources}/{profile}/{self.stores}/'
                path_file = self.name_file(path)
                self.get_src_for_download(path_file, profile)
                self.logger.info('it"s just a story')
        self.logger.info('actually no exists stories')
