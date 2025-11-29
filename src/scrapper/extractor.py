from config.app_config import Config

import requests
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

        return title, pdf_path

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\n\s*\n+', '\n', text)
        text = re.sub(r' +', ' ', text)

        text = text.replace("bcb.gov.br", "")

        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        return text.strip()

    def __save_pdf__(self, title: str, pdf_bytes: bytes):
        safe_title = re.sub(r'[^a-zA-Z0-9_-]+', '_', title)

        output_path = f"tmp/{safe_title}.pdf"

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"[INFO] PDF salvo em: {output_path}")
        self.__save__(safe_title)

        return output_path

    def __save__(self, title):

        with open(f'{self.config.data_file_path}', 'w', encoding='UTF-8') as file:
            file.write(title)
