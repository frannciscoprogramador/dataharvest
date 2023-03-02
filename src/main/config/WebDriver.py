from abc import ABC, abstractmethod


class WebDriver(ABC):
    @abstractmethod
    def open(self, url: str):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def current_url(self):
        pass

    @abstractmethod
    def by_css_selector(self, class_name: str, time):
        pass

    @abstractmethod
    def by_all_css_selector(self, class_name: str, time):
        pass

    @abstractmethod
    def find_element_by_xpath(self, xpath_name: str, time):
        pass

    @abstractmethod
    def all_by_css_selector(self, class_name: str, time):
        pass

    @abstractmethod
    def execute_script(self, script):
        pass

    @abstractmethod
    def execute_script_to_div(self, script, element):
        pass
