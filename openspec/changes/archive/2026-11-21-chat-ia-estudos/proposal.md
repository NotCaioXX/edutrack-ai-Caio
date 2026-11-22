# Proposal: Página de Chat com IA para Estudos e Técnicas de Aprendizagem

## Why

Os estudantes do EduTrack AI necessitam de um espaço interativo e integrado para conversar sobre seus estudos, tirar dúvidas conceituais, planejar rotinas de estudo e aprender novas técnicas de aprendizagem (como Feynman, Pomodoro, Active Recall e repetição espaçada). Uma página dedicada de chat com IA proporciona esse suporte pedagógico diretamente na aplicação.

## What Changes

- **Serviço de IA (`scripts/ai_tutor_service.py`)**:
  - Módulo simples em Python responsável por gerenciar a comunicação com o provedor de IA (Gemini API) usando a chave de API configurada no ambiente.
  - Definição do system prompt especializado em orientação de estudos e técnicas de aprendizagem em português brasileiro.
- **Página de Chat do Tutor IA (`pages/4_💬_Tutor_IA.py`)**:
  - Nova página Streamlit com interface de chat utilizando `st.chat_message` e `st.chat_input`.
  - Histórico de mensagens mantido na sessão (`st.session_state.messages`).
  - Integração visual com o padrão EduTrack AI (tema escuro, barra de navegação superior e sem uso de emojis nos textos).

## Capabilities

### New Capabilities
- `ai-study-tutor`: Capacidade de interagir com um assistente inteligente via chat para orientação acadêmica, suporte em técnicas de estudo e planejamento de rotina.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend/Scripts**:
  - Criação de `scripts/ai_tutor_service.py`
  - Criação de `pages/4_💬_Tutor_IA.py`
  - Atualização do componente de navegação superior para incluir a nova página
- **Dependências**:
  - Adição do pacote `google-genai` (ou `google-generativeai`) nos requisitos
- **Backend/Xano**: Nenhuma alteração em tabelas ou APIs do Xano necessária.
