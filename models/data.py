import csv
import json
import logging
import os
import sqlite3
import tempfile
from typing import Any, Callable, Dict, List, Optional, Union


class Data:
    def __init__(self, data_name: str, data_path: str, data_table_name: str) -> None:
        self.data_name = data_name
        self.data_path = data_path
        self.data_table_name = data_table_name
        self.data: List[Dict[str, Any]] = []

    def load_data(self) -> None:
        try:
            if ".json" in self.data_path:
                with open(self.data_path, "r", encoding="utf-8") as file:
                    self.data = json.load(file)["logins"]
            else:
                with sqlite3.connect(self.data_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT * FROM {self.data_table_name}")
                    columns = [desc[0] for desc in cursor.description]
                    self.data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except FileNotFoundError:
            logging.info("%s %s not found", self.data_path, self.data_table_name)
        except json.JSONDecodeError:
            logging.info("Error decoding JSON in %s", self.data_path)
        except sqlite3.Error:
            logging.info("SQLite error in %s", self.data_path)

    def get_data(self) -> List[Dict[str, Any]]:
        return self.data

    def filter_data(
        self,
        columns: Union[List[str], str] = "all",
        ignored_types: Optional[List[str]] = None,
    ) -> None:
        if columns == "all":
            columns = self.get_all_columns()
        if ignored_types is None:
            ignored_types = []

        filtered_data = []
        for row in self.data:
            filtered_row = {}
            for column, value in row.items():
                if column in columns and type(value).__name__ not in ignored_types:
                    filtered_row[column] = value
            filtered_data.append(filtered_row)
        self.data = filtered_data

    def filter_cookies_data(self, host: str) -> List[Dict[str, Any]]:
        filtered_data = []
        for item in self.data:
            item_host = item.get("host")
            item_host_key = item.get("host_key")
            if (item_host and host in item_host) or (
                item_host_key and host in item_host_key
            ):
                filtered_data.append(item)
        return filtered_data

    def decrypt_column_data(
        self,
        saved_column: str,
        encrypted_column: str,
        decrypt_method: Callable[[Any, bytes], str],
        key: bytes,
    ) -> None:
        if self.data and encrypted_column not in self.data[0]:
            return

        decrypted_data = []
        for row in self.data:
            decrypted_row = row.copy()
            encrypted_value = decrypted_row[encrypted_column]
            decrypted_value = (
                decrypt_method(encrypted_value, key)
                if "".encode("utf-8") != encrypted_value
                else ""
            )
            decrypted_row[saved_column] = decrypted_value
            del decrypted_row[encrypted_column]
            decrypted_data.append(decrypted_row)
        self.data = decrypted_data

    def get_all_columns(self) -> List[str]:
        return list(self.data[0].keys()) if self.data else []

    @classmethod
    def save_data_as_json(
        cls, data: List[Dict[str, Union[str, int]]], filename: str
    ) -> None:
        normal_filename = os.path.normpath(filename)
        filepath = os.path.join(tempfile.gettempdir(), normal_filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logging.info("Saved data to JSON file %s", filepath)

    @classmethod
    def save_data_as_csv(
        cls, data: List[Dict[str, Union[str, int]]], filename: str
    ) -> None:
        normal_filename = os.path.normpath(filename)
        filepath = os.path.join(tempfile.gettempdir(), normal_filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        keys = data[0].keys() if data else []
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logging.info("Saved data to CSV file %s", filepath)
