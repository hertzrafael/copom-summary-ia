from scrapper.extractor import Extractor
from view.principal_view import PrincipalView

import streamlit as st

def main():
    extractor = Extractor()

    st.title('Sumário COPOM')
    PrincipalView(extractor).run()


if __name__ == '__main__':
    main()
