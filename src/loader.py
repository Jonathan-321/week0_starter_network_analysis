import argparse
import copy
import io
import json
import os
import shutil
from datetime import datetime
from time import sleep

import pandas as pd
from pick import pick  # type: ignore


# Create wrapper classes for using _sdk in place of newser
class NewsDataLoader:
    """
    news exported data IO class.

    When you open news exported ZIP file, each channel or direct message
    will have its own folder. Each folder will contain messages from the
    conversation, organised by date in separate JSON files.

    You'll see reference files for different kinds of conversations:
    users.json files for all types of users that exist in the news workspace
    channels.json files for public channels,

    These files contain metadata about the conversations, including their names and IDs.

    For secruity reason, we have annonymized names - the names you will see are generated using faker library.

    """

    def __init__(self):
        """
        path: path to the slack exported data folder
        """

        self.data = {}

    def load_data(self, path):
        """
        write a function to load all the messages from all the channels
        """

        if path not in self.data:
            self.data[path] = pd.read_csv(path)
        return self.data[path]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export News history")
    parser.add_argument("--zip", help="Name of a zip file to import")
    args = parser.parse_args()
