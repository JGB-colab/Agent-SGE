import re
import yaml
import json
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
ROOT = Path(__file__).resolve().parent

from service.agent.system import InitAgent

TOOL_CALL_LEAK_PATTERN = re.compile(r'"name"\s*:\s*"\w+".{0,60}"parameters"', re.IGNORECASE | re.DOTALL)
TOOL_CALL_LEAK_TERMOS = ("sql_db_query", "sql_db_schema", "sql_db_list_tables")

def carregar_golden_set():
    with open(ROOT / "golden_set.yaml") as f:
        return yaml.safe_load(f)

def vazou_tool_call(resposta):
    """Detecta quando a chamada de ferramenta (JSON cru) vaza para a resposta final
    em vez de o agente executar a tool e responder em linguagem natural."""
    if TOOL_CALL_LEAK_PATTERN.search(resposta):
        return True
    resposta_lower = resposta.lower()
    return any(termo in resposta_lower for termo in TOOL_CALL_LEAK_TERMOS)

def avaliar_resposta(resposta, esperado):
    resultados = {}

    # Checagem estrutural: aplica-se a toda resposta, independente do golden_set.
    # Uma resposta que vaza a chamada de tool (JSON cru) nao e uma resposta valida
    # para o usuario, mesmo que contenha as palavras-chave esperadas.
    resultados["resposta_nao_vazou_tool_call"] = not vazou_tool_call(resposta)

    for termo in esperado["deve_conter"]:
        resultados[f"contem_{termo}"] = termo.lower() in resposta.lower()

    # Grounding factual: valores reais do banco que a resposta precisa citar.
    # Diferente de "deve_conter" (termos genericos), aqui e o fato correto -
    # pega alucinacao que "parece" certa mas inventa dado que nao existe no banco.
    for termo in esperado.get("deve_conter_valor_real", []):
        resultados[f"contem_valor_real_{termo}"] = termo.lower() in resposta.lower()

    for termo in esperado["nao_deve_conter"]:
        resultados[f"nao_contem_{termo}"] = termo.lower() not in resposta.lower()

    passou = all(resultados.values())
    return passou , resultados

def rodar_evals(modelo="gpt-3.5-turbo"):
    golden_set = carregar_golden_set()
    agente = InitAgent(modelo)

    resultados = []
    for caso in golden_set['casos']:
        output = agente.invoke({"messages": [("user", caso['pergunta'])]})
        resposta = output["messages"][-1].content
        passou , detalhes = avaliar_resposta(resposta , caso['resposta_esperada'])

        resultados.append({
            "id": caso["id"],
            "pergunta": caso["pergunta"],
            "passou": passou,
            "detalhes": detalhes,
            "resposta": resposta
        })
        status = "S" if passou else "N"
        print(f"{status} Caso {caso['id']}: {caso['pergunta'][:50]}...")
    total = len(resultados)
    passou = sum(1 for r in resultados if r['passou'])
    print(f"\nResultado: {passou}/{total} casos passaram")

    output_file = ROOT / f"evals_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "modelo": modelo,
            "total_casos": total,
            "casos_passaram": passou,
            "taxa_sucesso": f"{(passou/total*100):.1f}%",
            "resultados": resultados
        }, f, indent=2, ensure_ascii=False)
    print(f"[OK] Resultados salvos em: {output_file.name}")
    return resultados

if __name__ == "__main__":
    modelo = sys.argv[1] if len(sys.argv) > 1 else "gpt-3.5-turbo"
    rodar_evals(modelo)