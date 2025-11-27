class Config:

    def __init__(self):
        self.base_url = 'https://www.bcb.gov.br/'
        self.url = f'{self.base_url}api/servico/sitebcb/atascopom/ultimas?quantidade=1&filtro='
        self.data_file_path = '../data.txt'
        self.last_content_path = '../last_content.txt'
