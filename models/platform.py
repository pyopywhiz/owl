from typing import List

from models.browser import Browser


class Platform:
    def __init__(self, platform_name: str):
        self.platform_name: str = platform_name
        self.browsers: List[Browser] = []

    def create_browser(self, browser: Browser) -> None:
        self.browsers.append(browser)

    def get_browsers(self) -> List[Browser]:
        return self.browsers
