import streamlit as st
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from service.agent.system import InitAgent
ROOT_PROJECT = Path(__file__).resolve().parent


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


agent = InitAgent(select_model)

if st.button("Consultar"):
    
    if user_question:
        with st.spinner("Consultando o banco de dados.."):
            st.write("Processando sua pergunta...")
            output = agent.invoke({"messages": [("user", user_question)]})
            st.markdown(output["messages"][-1].content)
    else:
        st.warning("Por favor, digite uma pergunta antes de consultar.")