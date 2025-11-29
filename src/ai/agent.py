from agno.agent import Agent
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

class UserAgent(Agent):

    def __init__(self):
        self.current = 0
        self.GROQ_API_KEY = None
        self.GEMINI_API_KEY = None
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
                cidadão comum.
            """
        )

        self.create_knowledge()
        self.switch_model()

    def switch_model(self):
        self.current = 0 if self.current + 1 >= len(self.available_models) else self.current + 1

        self.model_id = self.available_models[self.current]
        self.model = Groq(id=self.model_id, api_key=self.GROQ_API_KEY, temperature=0.2)

        print(f'[INFO] O modelo foi trocado para {self.model_id}')

    def create_knowledge(self):
        knowledge = Knowledge(
            vector_db=ChromaDb(
                collection="vectors",
                path="tmp/chromadb",
                persistent_client=True,
                embedder=HuggingfaceCustomEmbedder(api_key=self.GEMINI_API_KEY, id='sentence-transformers/all-MiniLM-L6-v2')
            ),
            contents_db = SqliteDb(db_file="tmp/my_knowledge.db")
        )

        self.knowledge = knowledge
        self.add_knowledge_to_context=True
        self.search_knowledge=True

    def add_knowledge(self, meet, pdf_path):

        if self.__document_exists__(meet):
            return

        reader = PDFReader(chunk_size=512)

        self.knowledge.add_content(
            path=pdf_path,
            reader=reader
        )

    def __document_exists__(self, name: str) -> bool:
        collection = self.knowledge.vector_db.client.get_collection("vectors")

        result = collection.query(
            query_texts=["check"],
            where={"file_name": name}
        )

        print(result)

        return len(result["ids"][0]) > 0

    def run_prompt(self, prompt):
        print(f'[INFO] Rodando prompt: {prompt}')
        try:
            response = self.run(f"{prompt}")
            return str(response.content)
        except Exception as e:
            print(f"[ERRO] {e} -> tentando próximo modelo...")
            self.switch_model()
            return self.run_prompt(prompt)
