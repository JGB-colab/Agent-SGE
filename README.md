# 📦 StockAI: Gestão de Estoque Inteligente com RAG

## 📌 Visão Geral
O **StockAI** é uma aplicação integrada que une o gerenciamento de inventário tradicional com o poder das LLMs. O diferencial deste projeto é permitir que o gestor não apenas veja números, mas **converse com os dados do seu estoque** para obter insights rápidos sobre reposição, tendências e descrições de produtos.

## 🎯 Objetivos do Projeto
1.  **Eficiência Operacional:** Reduzir o tempo de consulta a tabelas complexas através de uma interface de chat.
2.  **Busca Semântica:** Encontrar produtos por contexto (ex: "preciso de algo para limpeza de escritórios") e não apenas por código SKU.
3.  **Análise de Dados:** Utilizar IA para identificar produtos parados ou com baixo nível de estoque.

## 🛠️ Stack Tecnológica
-   **Interface e App:** [Streamlit](https://streamlit.io/) (Frontend e Backend integrados).
-   **Banco de Dados Relacional:** [SQLite](https://www.sqlite.org/) (Armazenamento de produtos, quantidades e transações).
-   **Banco de Dados Vetorial:** [ChromaDB](https://www.trychroma.com/) (Armazenamento de embeddings para busca semântica e RAG).
-   **Orquestração de IA:** [LangChain](https://python.langchain.com/) (Integração entre LLM, SQL e Vetores).
-   **LLM:** OpenAI GPT-3.5/4 (via API).

## 🚀 Funcionalidades Principais
-   **Painel de Inventário:** Cadastro, edição e visualização de produtos salvos no SQLite.
-   **Chat com o Estoque (SQL Agent):** Interface onde o usuário pergunta "Qual o valor total do meu estoque hoje?" e a IA traduz para uma query SQL, executa no SQLite e responde em linguagem natural.
-   **Busca por Similaridade (RAG):** Utiliza o ChromaDB para encontrar produtos baseando-se na descrição técnica, ajudando a encontrar substitutos ou itens relacionados.
-   **Alertas Inteligentes:** Sugestões automáticas de compra baseadas em regras de negócio processadas pela IA.

## 📂 Estrutura do Projeto
```text
stock-ai/
├── app.py              # Arquivo principal (Streamlit)
├── database.db         # Lógica de conexão e queries SQLite
├── requirements.txt    # Dependências do projeto
```

## 🔧 Como Rodar
1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/stock-ai.git
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure sua chave da OpenAI:**
    Crie um arquivo `.env` ou configure nos secrets do Streamlit:
    ```text
    OPENAI_API_KEY=sua_chave_aqui
    ```
4.  **Inicie a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📈 Evoluções Futuras
-   Implementação de previsão de demanda (Time Series) integrada ao chat.
-   Leitura de Notas Fiscais via OCR para entrada automática de estoque.
-   Migração para PostgreSQL/pgvector conforme a escala do projeto aumentar.

---
