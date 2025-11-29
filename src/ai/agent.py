from agno.agent import Agent
from agno.exceptions import ModelProviderError
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

class UserAgent(Agent):

    def __init__(self):
        self.current = 0
        self.available_models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3-32b",
            "deepseek-r1-distill-llama-70b",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-guard-4-12b",
            "meta-llama/llama-prompt-guard-2-22m",
            "meta-llama/llama-prompt-guard-2-86m"
        ]

        super().__init__(
            role="""
                Você é uma Inteligência Artifical para ajudar com relação às dúvidas sobre as últimas atas do COPOM. 
                Seu principal objetivo é trazer a informação da ata com uma linguagem que até mesmo quem não entende do
                assunto consiga entender, assim como trazer os impactos dos resultados da ata irá trazer na vida do
                cidadão comum. Suas respostas devem possuir no máximo 400 caracteres, então seja objetivo! Se for
                qualquer outro assunto que não seja sobre temas relacionados à ata do COPOM, você deve dizer que não pode
                ajudar o usuário.
            """
        )

        self.create_knowledge()
        self.switch_model(force_change=False)

    def switch_model(self, force_change=True):

        if 'model' in st.session_state and not force_change:
            self.model_id = st.session_state.model
            print(f'[INFO] O modelo {self.model_id} mantém sendo usado.')
        else:
            self.current = 0 if self.current + 1 >= len(self.available_models) else self.current + 1
            self.model_id = self.available_models[self.current]
            print(f'[INFO] O modelo foi trocado para {self.model_id}')


        if 'groq_key' not in st.session_state:
            print('Você precisa inserir uma chave do Groq.')
            return

        groq_key = st.session_state.get('groq_key')

        print(f'usando modelo {self.model_id} com a key {groq_key}')
        self.model = Groq(id=self.model_id, api_key=groq_key, temperature=0.2)
        st.session_state.model = self.model_id


    def create_knowledge(self):

        if 'hugging_face_key' not in st.session_state:
            print('Você precisa inserir uma chave do Hugging Face.')
            return

        knowledge = Knowledge(
            vector_db=ChromaDb(
                collection="vectors",
                path="tmp/chromadb",
                persistent_client=True,
                embedder=HuggingfaceCustomEmbedder(api_key=self.__get_hugging_face_key__(),id='sentence-transformers/all-MiniLM-L6-v2')
            ),
            contents_db = SqliteDb(db_file="tmp/my_knowledge.db")
        )

        self.knowledge = knowledge
        self.add_knowledge_to_context=True
        self.search_knowledge=True

    def update_vector_embedder(self):

        if not self.knowledge or not self.knowledge.vector_db:
            return

        self.knowledge.vector_db.embedder = HuggingfaceCustomEmbedder(
            api_key=self.__get_hugging_face_key__(),
            id='sentence-transformers/all-MiniLM-L6-v2'
        )

    def add_knowledge(self, meet, pdf_path):

        if self.__document_exists__(meet):
            return

        reader = PDFReader(chunk_size=512)

        self.knowledge.add_content(
            path=pdf_path,
            reader=reader
        )

    def run_prompt(self, prompt):
        print(f'[INFO] Rodando prompt: {prompt}')
        try:
            response = self.run(f"{prompt}")
            return str(response.content)
        except ModelProviderError as e:
            raise ModelProviderError('Oops, algo deu errado! Verifique as api_keys passadas para o agente.')
        except Exception as e:
            print(f"[ERRO] {e} -> tentando próximo modelo....")
            self.switch_model()
            return self.run_prompt(prompt)

    def __document_exists__(self, name: str) -> bool:
        collection = self.knowledge.vector_db.client.get_collection("vectors")

        result = collection.query(
            query_texts=["check"],
            where={"file_name": name}
        )

        print(result)

        return len(result["ids"][0]) > 0

    def __get_groq_key__(self):
        return st.session_state.get('groq_key')

    def __get_hugging_face_key__(self):
        return st.session_state.get('hugging_face_key')