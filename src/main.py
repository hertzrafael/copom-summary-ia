from scrapper.extractor import Extractor
from view.principal_view import PrincipalView
from utils.copom_utils import get_or_request_pdf
from ai.agent import UserAgent

import streamlit as st
import asyncio

async def main():
    extractor = Extractor()
    agent = UserAgent()

    title, content = await get_or_request_pdf(extractor)

    st.title('Sumário COPOM')
    PrincipalView(extractor, agent, title, content).run()

    #print(title)
    #print(content)


if __name__ == '__main__':
    asyncio.run(main())
