from config.app_config import Config
from pypdf import PdfReader

import requests
import io


class Extractor:

    def __init__(self):
        self.config = Config()

    async def init(self) -> tuple[str, str]:
        print('Iniciando...')
        response = requests.get(self.config.url)
        content = response.json()

        target = content['conteudo'][0]
        url_file = target['Url']
        file = requests.get(f'{self.config.base_url}{url_file}')

        pdf_stream = io.BytesIO(file.content)
        reader = PdfReader(pdf_stream)

        title = target['Titulo']
        pdf_content = self.__get_text_from_pdf__(reader)
        self.__save__(title, pdf_content)

        return title, pdf_content

    def __get_text_from_pdf__(self, reader: PdfReader):
        return "\n\n".join(
            (page.extract_text() or "") for page in reader.pages
        )

    def __save__(self, title, content):

        with open(f'{self.config.data_file_path}', 'w', encoding='UTF-8') as file:
            file.write(title)

        with open(f'{self.config.last_content_path}', 'w', encoding='UTF-8') as file:
            file.write(content)
