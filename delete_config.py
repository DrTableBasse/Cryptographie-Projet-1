"""
Do not launch this script directly, only setup.sh should do it.
"""

import json

empty_config = {
                "host": "",
                "port": 22,
                "user": "",
                "password": "",

                "storedPath": "",
                "sendPath": ""
            }

with open('config.json', 'w') as f:
    json.dump(empty_config, f, indent=4)