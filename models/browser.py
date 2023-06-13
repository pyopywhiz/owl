import logging
import os
from typing import List

from models.profile import Profile


class Browser:
    def __init__(self, browser_name: str, browser_path: str) -> None:
        self.browser_path: str = browser_path
        self.browser_name: str = browser_name
        self.profiles: List[Profile] = []

    def create_profile(self, profile: Profile) -> None:
        self.profiles.append(profile)

    def get_profiles(self) -> List[Profile]:
        return self.profiles

    def load_profiles(self, default_profiles: List[str]) -> None:
        expand_browser_path: str = (
            os.path.expanduser(self.browser_path)
            if self.browser_path[0] == "~"
            else os.path.expandvars(self.browser_path)
        )

        if not os.path.exists(expand_browser_path):
            logging.error("No such directory: %s", expand_browser_path)
        else:
            browser_directories: List[str] = [
                directory
                for directory in os.listdir(expand_browser_path)
                if os.path.isdir(os.path.join(expand_browser_path, directory))
            ]

            browser_profiles: List[str] = [
                directory
                for directory in browser_directories
                if any(default in directory for default in default_profiles)
            ]

            self.profiles = [
                Profile(os.path.join(expand_browser_path, profile))
                for profile in browser_profiles
            ]
