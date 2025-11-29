from config.app_config import Config

import os
import hashlib

config = Config()

async def get_or_request_pdf(extractor):

    name = None
    content = None

    if os.path.exists(f'{config.data_file_path}') and os.path.exists(f'{config.last_content_path}'):

        with open(f'{config.data_file_path}', 'r', encoding='UTF-8') as file:
            name = file.read()

        #with open(f'{config.last_content_path}', 'r', encoding='UTF-8') as file:
        #    content = file.read()

        return name, content

    name, content = await extractor.init()

    return name, content

def hash_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()



