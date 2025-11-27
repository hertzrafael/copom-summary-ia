from config.app_config import Config

import streamlit as st
import asyncio


class PrincipalView:

    def __init__(self, extractor, title, content):
        self.extractor = extractor
        self.title = title
        self.content = content
        self.config = Config()

    def run(self):
        self.__sidebar__()
        self.__principal__()

    def __sidebar__(self):
        st.sidebar.header('Último COPOM carregado:')
        st.sidebar.subheader(f'{self.__get_last_copom_name__()}')

        st.sidebar.button('Atualizar COPOM', type='primary', use_container_width=True, on_click=self.__update_copom__)

    def __principal__(self):

        container = st.container(border=True)

        with container.chat_message(name='ai'):
            st.write("""
            Seja bem-vindo! Eu sou uma Inteligência Artifical para lhe ajudar com relação às suas dúvidas sobre as últimas atas do COPOM.
            \n Minha missão é trazer o acesso à informação e traduzir os textos técnicos, de forma que qualquer um, até mesmo aqueles que não
            possuem o conhecimento na área, consiga entender o que está escrito e o que impacta na vida do cidadão comum.
            \n Insira aqui a sua dúvida, estou pronta para responder!
        """)


        #st.chat_message(name='ai')
        prompt = st.chat_input(placeholder='Insira aqui sua mensagem')
        

    def __get_last_copom_name__(self) -> str:

        try:
            with open(f'{self.config.data_file_path}', 'r', encoding='UTF-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Nenhum'

    def __update_copom__(self):
        title, content = asyncio.run(self.extractor.init())

        self.title = title
        self.content = content
