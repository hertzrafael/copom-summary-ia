from config.app_config import Config

import os
import hashlib

config = Config()

async def get_or_request_pdf(extractor):

    if os.path.exists(f'{config.data_file_path}'):
        return

    await extractor.init()

def hash_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()



