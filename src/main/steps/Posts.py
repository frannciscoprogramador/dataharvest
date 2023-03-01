from src.main.utils.Constants import GENERAL_WAITING_TIME, PAUSE_ANTI_BOT, GENERAL_EXPLICIT_WAIT_TIME
from src.main.config.WebDriver import WebDriver
from src.main.config.Logger import Logger
from src.main.steps.Download import Download
from src.main.config.SQL import SQL


class Posts:
    def __init__(self, web_driver: WebDriver, sql: SQL):
        self.logger = Logger('[           Posts           ]')
        self.web_driver = web_driver
        self.general_wait_time = GENERAL_WAITING_TIME
        self.download = Download(self.web_driver)
        self.pause_anti_bot = PAUSE_ANTI_BOT
        self.sql = sql

