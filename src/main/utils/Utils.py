import os
from src.main.config.Logger import Logger

logger = Logger('[           Utils           ]')


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"folder created in {path}")
    else:
        logger.info(f"the folder already exists in {path}")


def increment_filename(filepath):
    if not os.path.isfile(filepath):
        return filepath
    base_path, extension = os.path.splitext(filepath)
    i = 1
    while os.path.isfile(filepath):
        filepath = f"{base_path}_{i}{extension}"
        i += 1
    return filepath
