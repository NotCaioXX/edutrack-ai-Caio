# Design: Introdução ao Sistema e Controle de Acesso

## Context

O EduTrack AI atualmente permite que qualquer visitante navegue pelas páginas internas mesmo sem autenticação, embora as requisições para a API falhem ou mostrem telas vazias. Para oferecer uma experiência acolhedora e profissional, implementamos uma introdução ao sistema com restrição de acesso e fluxo de onboarding.

## Technical Architecture

```
Página Inicial.py
   │
   ├── Se NÃO logado:
   │      └── Tela de Boas-Vindas (Apresentação, recursos e botão para Perfil/Login)
   │
   └── Se LOGADO:
          ├── Se possui disciplinas: Dashboard completo (métricas, calendário, progresso)
          └── Se NÃO possui disciplinas: Banner/Card de Primeiros Passos (Cadastrar primeira matéria)

Páginas Internas (Disciplinas, Tarefas, Progresso, Tutor IA)
   │
   └── Verificação de autenticação no topo da página:
          ├── Se NÃO logado: Exibe aviso de bloqueio com botão de redirecionamento para Login
          └── Se LOGADO: Executa normalmente o conteúdo da página
```

## Decisions

1. **Padrão de Autenticação Centralizado**:
   - Criar função utilitária `require_auth()` em `components/navbar.py` ou módulo de autenticação para padronizar o bloqueio das páginas restritas.
2. **Página Inicial Condicional**:
   - Quando `not st.session_state.get("auth_token")`: renderiza a apresentação do EduTrack AI, destacando recursos de gestão acadêmica e tutor inteligente.
   - Quando autenticado: verifica se `subj_count == 0` para apresentar instruções de primeiros passos.
3. **Estilo e Diretrizes do Projeto**:
   - Manter tema escuro (#000000).
   - Ausência de emojis soltos no texto de apresentação.
   - Manter consistência com as logos existentes.
