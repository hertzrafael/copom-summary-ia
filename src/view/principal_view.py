from config.app_config import Config

import streamlit as st
import asyncio


class PrincipalView:

    def __init__(self, extractor, agent):
        self.extractor = extractor
        self.agent = agent
        self.config = Config()

        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def run(self):
        self.__sidebar__()
        self.__principal__()

    def __sidebar__(self):
        st.sidebar.header('Último COPOM carregado:')
        st.sidebar.subheader(f'{self.__get_last_copom_name__()}')

        st.sidebar.button('Atualizar COPOM', type='primary', use_container_width=True, on_click=self.__update_copom__)
        st.sidebar.divider()

        groq = st.sidebar.text_input('GROQ API')
        hugging_face = st.sidebar.text_input('HUGGING FACE API')

        st.session_state['groq_key'] = groq
        st.session_state['hugging_face_key'] = hugging_face

        self.agent.update_vector_embedder()

    def __principal__(self):

        container = st.container(border=True)

        with container.chat_message(name='ai'):
            st.write("""
            Seja bem-vindo! Eu sou uma Inteligência Artifical para lhe ajudar com relação às suas dúvidas sobre as últimas atas do COPOM.
            \n Minha missão é trazer o acesso à informação e traduzir os textos técnicos, de forma que qualquer um, até mesmo aqueles que não
            possuem o conhecimento na área, consiga entender o que está escrito e o que impacta na vida do cidadão comum.
            \n Insira aqui a sua dúvida, estou pronta para responder!
        """)


        for message in st.session_state.get('messages'):
            container.chat_message(name=message['name']).write(message['message'])

        prompt = st.chat_input(placeholder='Insira aqui sua mensagem', max_chars=300)
        if prompt:
            self.__insert_message__(container, 'user', prompt)

            try:
                result = self.agent.run_prompt(prompt)
                ai_response = result
            except Exception as e:
                ai_response = e.message

            self.__insert_message__(container, 'ai', ai_response)

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

    def __insert_message__(self, container, name, message):
        st.session_state.messages.append({'name': name, 'message': message})
        container.chat_message(name=name).write(message)