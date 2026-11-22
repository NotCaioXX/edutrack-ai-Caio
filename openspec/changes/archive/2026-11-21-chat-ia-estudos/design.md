# Design: Chat com IA para Estudos e Técnicas de Aprendizagem

## Context

O EduTrack AI é um aplicativo acadêmico construído com Streamlit e backend Xano. Para apoiar os estudantes na gestão do tempo e nos métodos de estudo, adiciona-se uma página de chat interativo com IA simples, mantendo consistência com o tema visual escuro e as regras de navegação da aplicação.

## Technical Architecture

```
Streamlit (pages/4_💬_Tutor_IA.py)
   │
   ├──> Componente de Chat (st.chat_message, st.chat_input)
   ├──> Histórico em st.session_state["messages"]
   │
   └──> scripts/ai_tutor_service.py
           │
           └──> Gemini API (gemini-1.5-flash / gemini-2.0-flash)
```

## Decisions

1. **Biblioteca e Modelo**:
   - Usar Gemini API por possuir modelo rápido (`gemini-1.5-flash` ou `gemini-2.0-flash`) e tier gratuito adequado para uso educacional.
   - Chave de API lida de variável de ambiente (`GEMINI_API_KEY`) com fallback amigável caso não esteja definida.

2. **Interface Streamlit**:
   - Manter a barra de navegação superior padrão (`render_top_navbar()`).
   - Respeitar as diretrizes de design do app (fundo escuro, sem emojis em textos explicativos, foco em clareza).
   - Armazenar o histórico no `st.session_state` da sessão para permitir conversa contínua com contexto.

3. **Tratamento de Exceções**:
   - Interceptar ausência de chave ou falhas de rede com aviso em banner explicativo (`st.warning` ou `st.error`) para não interromper a execução do app.
