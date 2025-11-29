from config.app_config import Config

import streamlit as st
import asyncio


class PrincipalView:

    def __init__(self, extractor, agent, title, content):
        self.extractor = extractor
        self.agent = agent
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
        st.sidebar.divider()

        groq = st.sidebar.text_input('GROQ API')
        gemini = st.sidebar.text_input('GEMINI API')

        self.agent.GROQ_API_KEY = groq
        self.agent.GEMINI_API_KEY = gemini

        self.agent.create_knowledge()

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
        prompt = st.chat_input(placeholder='Insira aqui sua mensagem', max_chars=300)

        if prompt:
            container.chat_message(name='user').write(prompt)
            result = self.agent.run_prompt(prompt)
            container.chat_message(name='ai').write(result)

    def __get_last_copom_name__(self) -> str:

        try:
            with open(f'{self.config.data_file_path}', 'r', encoding='UTF-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Nenhum'

    def __update_copom__(self):
        title, pdf_path = asyncio.run(self.extractor.init())

        self.title = title
        self.pdf_path = pdf_path

        self.agent.add_knowledge(title.split()[0].replace('ª', ''), pdf_path)