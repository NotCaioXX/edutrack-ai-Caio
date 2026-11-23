# Proposal: Introdução ao Sistema e Controle de Acesso para Usuários Não Logados

## Why

Atualmente no EduTrack AI, quando um visitante ou usuário não autenticado acessa o sistema, ele visualiza telas com métricas vazias ou calendários sem dados, e consegue navegar por páginas internas (como Disciplinas, Tarefas, Progresso e Tutor IA) onde as funcionalidades dependem de login. Além disso, novos usuários recém-cadastrados que não possuem nenhuma matéria ou tarefa precisam de instruções claras de boas-vindas e primeiros passos.

## What Changes

1. **Controle de Acesso (Bloqueio de Páginas Internas)**:
   - Usuários não logados (sem token de autenticação ativo) só poderão interagir com a **Página Inicial** e com a página de **Perfil** (para login ou cadastro).
   - Ao tentar acessar as páginas internas (`Disciplinas`, `Tarefas`, `Progresso`, `Tutor IA`), o sistema bloqueia o conteúdo exibindo aviso para fazer login/cadastro ou redireciona amigavelmente para a página de Perfil.
   - Na barra de navegação (`navbar.py`), links para páginas protegidas podem ser desabilitados/ocultados ou exibir feedback amigável quando o usuário não estiver autenticado.
2. **Página Inicial para Visitante Não Logado**:
   - Apresentar um painel de boas-vindas com a proposta do EduTrack AI, recursos disponíveis e botões claros convidando o usuário a fazer login ou criar sua conta.
3. **Página Inicial para Usuário Logado**:
   - Exibir o dashboard completo atual (métricas, calendário, progresso das matérias).
4. **Onboarding para Usuário Novo (Sem Matérias/Tarefas)**:
   - Se o usuário autenticado não tiver matérias ou tarefas cadastradas, exibir orientações em destaque ("Primeiros Passos") incentivando a cadastrar a primeira matéria e as primeiras tarefas.

## Capabilities

### New Capabilities
- `user-onboarding-access`: Controle de acesso para visitantes não autenticados e mensagens de onboarding na página inicial para novos estudantes.

### Modified Capabilities
<!-- None -->

## Impact

- **Frontend**:
  - `Página Inicial.py`
  - `components/navbar.py`
  - `pages/1_📚_Disciplinas.py`
  - `pages/2_📝_Tarefas.py`
  - `pages/3_📊_Progresso.py`
  - `pages/4_💬_Tutor_IA.py`
- **Backend/Xano**: Nenhuma alteração em schemas de banco necessária.
