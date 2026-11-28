"""
Módulo de serviço para integração com IA (Tutor de Estudos do EduTrack AI).
Compatível com chamadas REST diretas para a API do Google Gemini ou modo simulador/educacional.
"""

import os
import json
from typing import List, Dict, Any, Optional
import requests

DEFAULT_SYSTEM_INSTRUCTION = (
    "Você é o Tutor de Estudos e Produtividade do EduTrack AI. "
    "Seu papel é orientar o estudante em suas matérias, sugerir métodos eficientes de aprendizagem "
    "(como método Feynman, Técnica Pomodoro, Active Recall e Repetição Espaçada), ajudar na organização "
    "de rotinas e cronogramas, e tirar dúvidas conceituais. "
    "Responda sempre em português brasileiro de forma acolhedora, objetiva, prática e didática. "
    "Não utilize emojis exagerados. Mantenha formatação limpa em markdown com listas e tópicos."
)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def load_env_if_needed():
    """Garante o carregamento do arquivo .env caso ainda não esteja carregado."""
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v


def get_gemini_api_key() -> Optional[str]:
    """Retorna a chave da API do Gemini prioritariamente de st.secrets (.streamlit/secrets.toml)
    com fallback para as variáveis de ambiente (.env)."""
    # 1. Tenta obter de st.secrets (arquivo .streamlit/secrets.toml)
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            val = str(st.secrets["GEMINI_API_KEY"]).strip().strip('"').strip("'")
            if val:
                return val
        if "GOOGLE_API_KEY" in st.secrets:
            val = str(st.secrets["GOOGLE_API_KEY"]).strip().strip('"').strip("'")
            if val:
                return val
    except Exception:
        pass

    # 2. Fallback para variáveis de ambiente (.env)
    load_env_if_needed()
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def generate_simulated_tutor_response(user_message: str) -> str:
    """
    Gera uma resposta didática de estudos caso nenhuma chave de API esteja configurada,
    permitindo que a interface seja demonstrada e testada imediatamente.
    """
    msg_lower = user_message.lower()

    if any(k in msg_lower for k in ["feynman", "tecnica feynman", "método feynman"]):
        return (
            "A **Técnica de Feynman** é um dos métodos mais eficientes para aprender profundamente qualquer conceito:\n\n"
            "1. **Escolha o conceito**: Anote o tema que você deseja dominar no topo de uma folha.\n"
            "2. **Ensine a uma criança**: Escreva uma explicação em termos extremamente simples, sem jargões ou termos difíceis.\n"
            "3. **Identifique as lacunas**: Onde você travou ou precisou recorrer ao material? Esses são seus pontos fracos.\n"
            "4. **Revise e simplifique**: Volte às suas fontes, refine sua explicação e crie analogias do dia a dia.\n\n"
            "*Dica do EduTrack:* Pegue uma disciplina cadastrada no seu painel e tente explicar a última tarefa para você mesmo em voz alta!"
        )

    if any(k in msg_lower for k in ["pomodoro", "tempo", "concentração", "foco"]):
        return (
            "A **Técnica Pomodoro** ajuda a manter o foco profundo e evitar fadiga mental:\n\n"
            "- **25 minutos de Foco Total**: Feche notificações, redes sociais e trabalhe exclusivamente na tarefa.\n"
            "- **5 minutos de Pausa Curta**: Levante, beba água, estique o corpo (sem telas).\n"
            "- **Repita 4 ciclos**: Ao final de 4 blocos de 25 minutos, faça uma **pausa longa de 15 a 30 minutos**.\n\n"
            "Para matérias com tarefas longas no EduTrack, divida a atividade em 2 ou 3 pomodoros."
        )

    if any(k in msg_lower for k in ["rotina", "cronograma", "organizar", "planejamento"]):
        return (
            "Para montar uma rotina de estudos sustentável e equilibrada:\n\n"
            "1. **Mapeie suas matérias**: Priorize matérias em que sua média está mais baixa ou com prazos próximos.\n"
            "2. **Blocos de tempo fixos**: Reserve horários consistentes do dia em que sua energia mental é maior.\n"
            "3. **Estudo ativo em vez de passivo**: Em vez de apenas reler resumos, resolva exercícios e faça testes práticos.\n"
            "4. **Revisões espaçadas**: Revise o conteúdo 24 horas depois, 7 dias depois e 30 dias depois.\n\n"
            "Você pode verificar suas tarefas pendentes na aba **Tarefas** do EduTrack para planejar o dia."
        )

    if any(k in msg_lower for k in ["active recall", "recordação ativa", "memorizar", "lembrar"]):
        return (
            "O **Active Recall (Recordação Ativa)** é o método com maior comprovação científica para retenção de memória:\n\n"
            "- Em vez de reler passivamente suas anotações, feche o caderno e tente escrever ou falar tudo o que você lembra.\n"
            "- Crie perguntas para si mesmo antes da aula e tente respondê-las depois.\n"
            "- Utilize flashcards (como o app Anki) para fórmulas, datas, vocabulário ou conceitos-chave.\n"
            "- Sempre force o cérebro a recuperar a informação da memória antes de olhar a resposta."
        )

    return (
        f"Excelente pergunta sobre seus estudos!\n\n"
        f"Ao estudar sobre *'{user_message}'*, recomendo adotar a abordagem de **estudo ativo**:\n"
        f"1. **Defina um objetivo claro**: O que exatamente você precisa ser capaz de resolver ou explicar ao fim da sessão?\n"
        f"2. **Divida em microtarefas**: Não tente absorver um capítulo inteiro de uma vez; separe por subtemas.\n"
        f"3. **Prática deliberada**: Faça ao menos 3 a 5 exercícios práticos aplicando a teoria.\n"
        f"4. **Autoavaliação**: Registre suas notas e progresso no EduTrack para acompanhar a evolução da sua média.\n\n"
        "*(Modo de Demonstração EduTrack ativo: Para ativar a IA em tempo real com o Google Gemini, configure a variável GEMINI_API_KEY no arquivo .env)*"
    )


def is_query_about_grades_or_academic_data(message: str) -> bool:
    """Verifica se a mensagem do usuário faz perguntas sobre notas, médias ou desempenho acadêmico."""
    msg = message.lower()
    keywords = [
        "minha nota", "minhas notas", "minha média", "minhas médias", "meu progresso",
        "como estou", "meu boletim", "como estão minhas matérias", "como está meu desempenho",
        "qual a minha nota", "qual é a minha nota", "qual a minha média", "qual é a minha média",
        "quanto tirei", "minhas tarefas concluídas", "minhas tarefas pendentes",
        "minha situação", "meu rendimento", "nota em", "média em"
    ]
    return any(k in msg for k in keywords)


def format_academic_context(user_info: Optional[Dict[str, Any]], progress_data: Optional[List[Dict[str, Any]]]) -> str:
    """Formata o contexto de progresso e notas do aluno para injeção no prompt da IA."""
    if not user_info and not progress_data:
        return ""

    student_name = user_info.get("name", "Estudante") if user_info else "Estudante"
    lines = [f"\n--- CONTEXTO ATUAL DO ESTUDANTE ({student_name}) NO EDUTRACK AI ---"]

    if not progress_data:
        lines.append("O estudante não possui disciplinas cadastradas no momento.")
    else:
        # Resumo geral
        tot_disciplinas = len(progress_data)
        tot_tarefas = sum(item.get("total_tasks", 0) for item in progress_data)
        tot_concluidas = sum(item.get("completed_tasks", 0) for item in progress_data)
        tot_pendentes = sum(item.get("pending_tasks", 0) for item in progress_data)

        # Média geral
        graded_items = [i for i in progress_data if i.get("average_grade") is not None and i.get("graded_tasks", 0) > 0]
        if graded_items:
            s_sum = sum(i["average_grade"] * i["graded_tasks"] for i in graded_items)
            s_cnt = sum(i["graded_tasks"] for i in graded_items)
            overall_avg = round(s_sum / s_cnt, 2)
            lines.append(f"Média Geral das Tarefas: {overall_avg}/10.0 (em {s_cnt} tarefas avaliadas)")
        else:
            lines.append("Média Geral: Ainda sem notas lançadas nas atividades concluídas.")

        lines.append(f"Total de Matérias: {tot_disciplinas} | Concluídas: {tot_concluidas}/{tot_tarefas} tarefas | Pendentes: {tot_pendentes}")
        lines.append("\nDetalhes por Disciplina:")

        for item in progress_data:
            s_name = item.get("subject_name", "Disciplina")
            c_tasks = item.get("completed_tasks", 0)
            t_tasks = item.get("total_tasks", 0)
            p_tasks = item.get("pending_tasks", 0)
            pct = item.get("progress_percentage", 0.0)
            avg = f"{item['average_grade']:.1f}/10.0" if item.get("average_grade") is not None else "Sem nota"
            graded_cnt = item.get("graded_tasks", 0)

            lines.append(
                f"- **{s_name}**: Média de Notas: {avg} ({graded_cnt} avaliadas) | "
                f"Progresso: {pct}% ({c_tasks}/{t_tasks} concluídas, {p_tasks} pendentes)"
            )

    lines.append("--- FIM DO CONTEXTO ATUAL DO ESTUDANTE ---\n")
    return "\n".join(lines)


def call_ai_tutor(
    messages: List[Dict[str, str]],
    model: str = "gemini-3.5-flash-lite",
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
    academic_context: Optional[str] = None
) -> str:
    """
    Envia o histórico de mensagens para a API Gemini ou recorre ao simulador didático
    se a chave não estiver configurada.
    """
    api_key = get_gemini_api_key()

    # Se não houver chave configurada, usa o simulador didático integrado
    if not api_key:
        last_user_message = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_message = m.get("content", "")
                break
        return generate_simulated_tutor_response(last_user_message)

    models_to_try = [model]
    if model != "gemini-3.5-flash":
        models_to_try.append("gemini-3.5-flash")

    last_error = ""

    for target_model in models_to_try:
        try:
            url = GEMINI_API_URL.format(model=target_model) + f"?key={api_key}"

            # Monta payload compatível com Gemini REST API
            contents = []
            for msg in messages:
                role = "user" if msg.get("role") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })

            # Se houver contexto acadêmico fornecido, adiciona às instruções do sistema
            full_system_instruction = system_instruction
            if academic_context:
                full_system_instruction += f"\n\n{academic_context}"

            payload: Dict[str, Any] = {
                "contents": contents,
                "systemInstruction": {
                    "parts": [{"text": full_system_instruction}]
                },
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 4096,
                }
            }

            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            continue
        except Exception as e:
            last_error = str(e)
            continue

    if last_error:
        return f"Erro de comunicação com a IA: {last_error}. Verifique sua conexão e a chave GEMINI_API_KEY."
    return "Não foi possível obter uma resposta do modelo no momento. Tente novamente."
