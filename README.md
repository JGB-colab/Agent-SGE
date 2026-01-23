---

# 🛡️ AI Credit Risk Commander: Automação End-to-End de Risco e Compliance

> **Impacto de Negócio:** Redução do Time-to-Decision de **14 dias para 24 horas** e mitigação de risco operacional através de Agentes de IA e Machine Learning.

---

## 1. O Problema de Negócio (The Business Challenge)
A **Lending-Elite Fintech** enfrenta um gargalo crítico em sua operação de crédito. O processo de análise de novos tomadores é manual, levando em média **14 dias** para uma resposta final. Além disso, a política de crédito é complexa (contida em extensos PDFs de compliance), o que gera inconsistência nas aprovações e perdas financeiras por inadimplência não detectada.

**O objetivo deste projeto é:**
1.  **Automatizar o Score de Crédito** utilizando modelos preditivos.
2.  **Identificar Fraudes e Anomalias** de forma proativa (Autoencoders).
3.  **Implementar um Agente de IA** que consulte a política de compliance (RAG) e emita um parecer final fundamentado, reduzindo o ciclo total para **menos de 1 dia**.

---

## 2. Estratégia de Solução (The Roadmap)

Para este desafio, utilizei o dataset real do **LendingClub** (Kaggle), estruturando a solução em 3 camadas de inteligência:

### Camada 01: Motor de Risco (Machine Learning Clássico)
*   **EDA Avançada:** Identificação dos principais drivers de inadimplência (DTI, FICO score, anual income).
*   **Modelagem:** Treinamento de um classificador **XGBoost** para prever o `loan_status` (Default vs Fully Paid).
*   **Métricas de Performance:** Foco em **Precision-Recall** e **KS (Kolmogorov-Smirnov)** para garantir a segurança da carteira.

### Camada 02: Detecção de Anomalias (Deep Learning)
*   Uso de **Autoencoders** para identificar padrões de comportamento atípicos em pedidos de crédito que burlam as regras tradicionais de scoring.

### Camada 03: Agente de Compliance (GenAI / LLMs)
*   **Arquitetura RAG:** Indexação da política de crédito em um banco de vetores (**ChromaDB**).
*   **Agente Decisor:** Implementação via **LangChain** que recebe o score do modelo (Camada 01) e o perfil do cliente, consulta as normas no banco de vetores e gera uma justificativa de aprovação/reprovação em linguagem natural.

---

## 3. Top 3 Insights de Negócio
1.  **Agilidade é Lucro:** A redução de 93% no tempo de análise permite que a fintech capture bons clientes antes da concorrência, aumentando o GMV projetado.
2.  **Risco Oculto:** O modelo de Autoencoder identificou que 5% dos clientes "aprovados" por regras simples possuíam padrões de gasto anômalos, evitando um prejuízo estimado de R$ X.
3.  **Explicabilidade:** O uso de Agentes de IA resolve o problema da "caixa preta" do ML, fornecendo ao regulador uma justificativa clara para cada decisão de crédito.

---

## 4. Stack Tecnológica & Engenharia
*   **Linguagem:** Python 3.10+
*   **Processamento de Dados:** DuckDB (Alta performance local) e Pandas.
*   **IA & ML:** Scikit-learn, XGBoost, LangChain, Google Gemini API.
*   **Vector Store:** ChromaDB.
*   **Engenharia de Sistemas:** Integração de serviços via **FastAPI** e arquitetura de comunicação eficiente (conceitos de gRPC aplicados à latência do Agente).

---

## 5. Como Executar o Projeto (Hands-on)
1.  **Clone o repositório:** `git clone ...`
2.  **Instale as dependências:** `pip install -r requirements.txt`
3.  **Download do Dataset:** Obtenha o `lending_club_loans.csv` no Kaggle e coloque na pasta `/data`.
4.  **Execute a interface:** `streamlit run app/main.py`

---

### 📫 Contato e Networking
**João Gabriel** - [LinkedIn](https://linkedin.com/in/joaogabrielborges)
---
