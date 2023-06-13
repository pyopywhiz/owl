import os
from typing import List, Optional

from models.data import Data


class Profile:
    def __init__(self, profile_path: str):
        self.profile_path: str = profile_path
        self.profile_name: str = os.path.basename(self.profile_path)
        self.profile_data: List[Data] = []

    def create_data(self, data: Data) -> None:
        self.profile_data.append(data)

    def get_profile_data(self) -> List[Data]:
        return self.profile_data

    def get_profile_data_by_data_name(self, data_name: str) -> Optional[Data]:
        for data in self.profile_data:
            if data.data_name == data_name:
                return data
        return None
