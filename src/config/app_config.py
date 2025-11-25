class Config:

    def __init__(self):
        self.base_url = 'https://www.bcb.gov.br/'
        self.url = f'{self.base_url}api/servico/sitebcb/atascopom/ultimas?quantidade=1&filtro='
