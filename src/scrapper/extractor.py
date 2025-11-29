from config.app_config import Config
from pypdf import PdfReader

import requests
import io
import re


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

        title = target['Titulo']
        pdf_path = self.__save_pdf__(title, file.content)


        #pdf_stream = io.BytesIO(file.content)
        #reader = PdfReader(pdf_stream)

        #title = target['Titulo']
        #pdf_content = self.clean_text(self.__get_text_from_pdf__(reader))
        #self.__save__(title, pdf_content)

        return title, pdf_path

    def __get_text_from_pdf__(self, reader: PdfReader):
        return "\n\n".join(
            (page.extract_text() or "") for page in reader.pages
        )

    def clean_text(self, text: str) -> str:
        # Remove múltiplos espaços e linhas vazias repetidas
        text = re.sub(r'\n\s*\n+', '\n', text)
        text = re.sub(r' +', ' ', text)

        # Remove cabeçalhos repetidos
        text = text.replace("bcb.gov.br", "")

        # Remove numeração solta de página
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        return text.strip()

    def __save_pdf__(self, title: str, pdf_bytes: bytes):
        safe_title = re.sub(r'[^a-zA-Z0-9_-]+', '_', title)

        output_path = f"tmp/{safe_title}.pdf"

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"[INFO] PDF salvo em: {output_path}")

        return output_path

    def __save__(self, title, content):

        with open(f'{self.config.data_file_path}', 'w', encoding='UTF-8') as file:
            file.write(title)

        #with open(f'{self.config.last_content_path}', 'w', encoding='UTF-8') as file:
        #    file.write(content)
