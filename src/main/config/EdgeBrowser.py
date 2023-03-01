from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from src.main.config.WebDriver import WebDriver
from abc import ABC


class EdgeBrowser(WebDriver, ABC):
    def __init__(self):
        edge_options = Options()
        # edge_options.add_argument("--headless")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-browser-side-navigation")
        edge_options.add_argument("--disable-session-crashed-bubble")
        edge_options.add_argument("--disable-restore-session-state")
        edge_options.add_argument("--disable-logging")
        edge_options.add_argument("--disable-background-timer-throttling")
        edge_options.add_argument("--disable-backgrounding-occluded-windows")
        edge_options.add_argument("--disable-renderer-backgrounding")
        edge_options.add_argument("--disable-breakpad")
        edge_options.add_argument("--ignore-certificate-errors")
        edge_options.add_argument("--allow-running-insecure-content")
        edge_options.add_argument("--disable-features=site-per-process")
        edge_options.add_argument("--user-data-dir=/home/xyz/.config/microsoft-edge-dev/Default")
        self.driver = webdriver.Edge(service=Service(executable_path="msedgedriver"), options=edge_options)

    def open(self, url: str):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.quit()

    def current_url(self):
        return self.driver.current_url

    def by_css_selector(self, class_name: str, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, class_name)))
        except:
            return False

    def by_all_css_selector(self, class_name: str, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, class_name)))
        except:
            return False

    def find_element_by_xpath(self, xpath_name: str, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((By.XPATH, xpath_name)))
        except:
            return False

    def all_by_css_selector(self, class_name: str, time):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, class_name)))
        except:
            return False
