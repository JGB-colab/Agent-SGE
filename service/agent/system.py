
from pathlib import Path
from .processing_docs import read_yaml
from langchain.agents import create_agent


from langchain_core.messages import SystemMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

OLLAMA_PREFIXES = ("phi", "mistral", "llama")

class InitAgent():
    def __init__(self, select_model: str) -> None:

        description = read_yaml().get('description')
        if isinstance(description, list):
            description = description[0]
        system_prompt = SystemMessage(content=description)

        # Criando modelos e conexões
        if select_model.startswith(OLLAMA_PREFIXES):
            model = ChatOllama(model=select_model, temperature=0.1)
        else:
            model = ChatOpenAI(model=select_model, temperature=0.1)
        db_path = Path(__file__).resolve().parents[2] / "estoque.db"
        db_uri = db_path.as_posix()
        db = SQLDatabase.from_uri(f"sqlite:///{db_uri}",
                                include_tables =['Products', 'Orders', 'Order Details'],
                                sample_rows_in_table_info = 3)

        toolkit = SQLDatabaseToolkit(
            db = db,
            llm = model,
            )

        self.agent = create_agent(
            model = model,
            tools = toolkit.get_tools(),
            system_prompt= system_prompt,
        )

    def invoke(self, input_data):
        return self.agent.invoke(input_data)