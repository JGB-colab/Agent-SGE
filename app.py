import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langsmith import Client 
from langchain_openai import  ChatOpenAI, OpenAIEmbeddings
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit 
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage

load_dotenv(find_dotenv())
persistent_directory = 'vector_db' # persistir a base de dados localmente


st.set_page_config(page_title = "Agent-SGE", page_icon = '🤖')

st.title("Agente SGE: App Streamlit para Gerenciamento de Estoque")
st.header("Assitente de estoque")

model_options= ['gpt-3.5-turbo', 'gpt-4']
select_model = st.sidebar.selectbox("Selecione o modelo",
                        options = model_options)

st.sidebar.markdown("## Sobre")
st.sidebar.markdown("Este é um aplicativo de gerenciamento de estoque que utiliza um agente inteligente para ajudar a organizar e controlar o estoque de uma empresa. O agente é capaz de responder a perguntas sobre o estoque, fornecer informações sobre produtos, e ajudar a tomar decisões relacionadas ao gerenciamento de estoque.")

st.write("Faça perguntas sobre o estoque de produtos, preços e reposições")
user_question = st.text_input("Digite sua pergunta aqui", key="input")

# Criando modelos e conexões
model = ChatOpenAI(model = select_model, 
                   temperature = 0.1)
client = Client()
system_prompt = client.pull_prompt("hwchase17/react")

db = SQLDatabase.from_uri("sqlite:///estoque.db")

toolkit = SQLDatabaseToolkit(
    db = db,
    llm = model,
    )

mensagem_sistema = SystemMessage(
    content='''
    Use as ferramentas necessárias para responder as perguntas realacionadas ao
    estoque de produtos e realtórios conforme solicitado pelo usuário, você fonecerá
    insights sobre produtos e preços.
    A resposta final deve ter uma formatação amigável de visulização para o usuário.
    Sempre responda em português brasileiro.
    '''
) 
agent = create_agent(
    model = model,
    tools = toolkit.get_tools(),
    system_prompt= mensagem_sistema,    
)

for step in agent.stream(
    {"messages": [{"role": "user", "content": user_question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print() 


if st.button("Consultar"):
    if user_question:
        with st.spinner("Consultando o banco de dados.."):
            st.write("Processando sua pergunta...")
            output = agent.invoke({"messages": [("user", user_question)]})
            st.markdown(output["messages"][-1].content)
    else:
        st.warning("Por favor, digite uma pergunta antes de consultar.")