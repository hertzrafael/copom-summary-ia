from src.config.app_config import Config
from pypdf import PdfReader

import requests
import io

class Extractor:

    def __init__(self):
        self.config = Config()

    def init(self, url) -> str:
        response = requests.get('https://www.bcb.gov.br/api/servico/sitebcb/atascopom/ultimas?quantidade=1&filtro=')
        content = response.json()

        url_file = content['conteudo'][0]['Url']
        file = requests.get(f'{self.config.base_url}{url_file}')

        pdf_stream = io.BytesIO(file.content)
        reader = PdfReader(pdf_stream)

        return self.__get_text_from_pdf__(reader)

    def __get_text_from_pdf__(self, reader: PdfReader):
        return "\n\n".join(
            (page.extract_text() or "") for page in reader.pages
        )

print(Extractor().init(Config().url))