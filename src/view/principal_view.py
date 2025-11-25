import streamlit as st


class PrincipalView:

    def __init__(self, extractor):
        self.extractor = extractor

    def run(self):
        self.__sidebar__()

    def __sidebar__(self):
        st.sidebar.header('Último COPOM carregado:')
        st.sidebar.subheader(f'{self.__get_last_copom_name__()}')

        st.sidebar.button('Atualizar COPOM', type='primary', use_container_width=True, on_click=self.extractor.init)

    def __get_last_copom_name__(self) -> str:

        try:
            with open('../data.txt', 'r', encoding='UTF-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Nenhum'
