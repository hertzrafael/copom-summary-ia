from config.app_config import Config
from pypdf import PdfReader

import requests
import io


class Extractor:

    def __init__(self):
        self.config = Config()

    def init(self) -> str:
        print('Iniciando...')
        response = requests.get(self.config.url)
        content = response.json()

        target = content['conteudo'][0]
        url_file = target['Url']
        file = requests.get(f'{self.config.base_url}{url_file}')

        pdf_stream = io.BytesIO(file.content)
        reader = PdfReader(pdf_stream)

        self.__save_title__(target['Titulo'])

        return self.__get_text_from_pdf__(reader)

    def __get_text_from_pdf__(self, reader: PdfReader):
        return "\n\n".join(
            (page.extract_text() or "") for page in reader.pages
        )

    def __save_title__(self, title):

        with open('../data.txt', 'w', encoding='UTF-8') as file:
            file.write(title)
