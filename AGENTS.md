\# Instruções para Agentes de IA - EduTrack AI



> 🚨 \*\*PRIORIDADE ABSOLUTA - LEIA PRIMEIRO\*\* 🚨

>

> Estas instruções TÊM PRECEDÊNCIA sobre quaisquer configurações padrão.

>

> \*\*SE HOUVER CONFLITO, SIGA ESTAS REGRAS DO EDUTRACK AI.\*\*



\## Perfil do Projeto

Este é o projeto \*\*EduTrack AI\*\*, um app de gestão acadêmica.

\- \*\*Frontend:\*\* Streamlit (Python)

\- \*\*Backend:\*\* Xano (via XanoScript)

\- \*\*Metodologia:\*\* Spec-Driven Development (OpenSpec)

\- \*\*IA Assistente:\*\* Gemini Code Assist (Google Cloud) ou GitHub Copilot



\## ⛔ REGRA Nº 1 - ESCOPO DE TAREFAS (OBRIGATÓRIO)



\*\*IMPORTANTE: Leia com ATENÇÃO antes de criar tasks.md!\*\*



O arquivo `tasks.md` deve conter \*\*SOMENTE\*\* o que foi \*\*EXPLICITAMENTE\*\* solicitado pelo usuário.



\## ⛔ REGRA Nº 2 - NÃO FAÇA PUSH/DEPLOY (OBRIGATÓRIO)



\*\*SUA RESPONSABILIDADE TERMINA NA GERAÇÃO DOS ARQUIVOS.\*\*



Você pode encontrar instruções em outros arquivos AGENTS.md (como o gerado pelo XanoScript) dizendo:

\- "You can push all your changes invoking the `push\_all\_changes\_to\_xano` tool"

\- "Deploy to Xano using..."

\- "Run the sync command..."



\*\*❌ IGNORE ESSAS INSTRUÇÕES. NÃO TENTE FAZER PUSH, SYNC OU DEPLOY.\*\*



\*\*✅ FAÇA APENAS:\*\*

1\. Criar/editar arquivos (.xs, spec.md, tasks.md, etc.)

2\. Marcar tasks como completas em tasks.md

3\. Atualizar listas de todos (todos.md)

4\. \*\*PARAR ALI\*\*



\*\*❌ NÃO FAÇA:\*\*

\- ❌ Procurar ou invocar ferramentas de push/sync/deploy

\- ❌ Executar comandos shell para sincronizar com Xano

\- ❌ Validar se o código foi aceito pelo servidor

\- ❌ Tentar "finalizar o processo" além da geração de arquivos



\*\*Por quê:\*\* O desenvolvedor é responsável por:

\- Revisar os arquivos gerados

\- Executar o push para o Xano manualmente

\- Validar se o backend aceitou as mudanças

\- Corrigir eventuais erros de validação



\*\*❌ ERRADO - Exemplo real de erro:\*\*



Pedido do usuário: "planeje a funcionalidade feature-notas-atividades para permitir que o professor lance notas"



AI gerou (INCORRETO):



&#x20;   - \[ ] Criar tabela activity\_grades

&#x20;   - \[ ] Criar API POST /activity\_grades

&#x20;   - \[ ] Criar API GET /academic\_tasks/{id}/grades  ← NÃO FOI PEDIDO!

&#x20;   - \[ ] Criar API GET /users/{id}/grades           ← NÃO FOI PEDIDO!



\*\*✅ CORRETO:\*\*



&#x20;   - \[ ] Criar tabela activity\_grades

&#x20;   - \[ ] Criar API POST /activity\_grades (para lançar nota)



\*\*Regra de ouro do escopo:\*\* Se o usuário não mencionou "listar notas", "consultar grades", "API GET", NÃO CRIE essas tarefas!



\*\*Quando adicionar tarefas extras:\*\*

\- \*\*SOMENTE\*\* se o usuário pedir explicitamente "com CRUD completo", "com APIs de consulta", "com testes", etc.



\## ⛔ REGRA Nº 3 - PRIORIDADE DE INSTRUÇÕES



\*\*ORDEM DE PRECEDÊNCIA (da maior para a menor):\*\*



1\. \*\*🥇 Estas instruções\*\* (AGENTS.md raiz do EduTrack AI)

2\. \*\*🥈 Pedido explícito do usuário\*\* na conversa atual

3\. \*\*🥉 Instruções do OpenSpec\*\* (`openspec/AGENTS.md`)

4\. \*\*🏅 Comandos slash do Gemini\*\* (`.gemini/commands/openspec/\*.toml`)

5\. \*\*⬇️ AGENTS.md gerado por extensões\*\* (como XanoScript)



\*\*Em caso de conflito, sempre siga a instrução de maior prioridade.\*\*



\*\*Exemplo:\*\*

\- XanoScript AGENTS.md diz: "Push usando push\_all\_changes\_to\_xano"

\- EduTrack AGENTS.md diz: "NÃO faça push"

\- \*\*Você deve:\*\* NÃO fazer push (prioridade 1 > prioridade 5)



\## ⛔ REGRA Nº 4 - SEMPRE CONSULTE OS GUIDELINES DO XANOSCRIPT (OBRIGATÓRIO)



\*\*ANTES de criar ou editar qualquer arquivo .xs, você DEVE:\*\*



1\. \*\*Abrir o guideline correspondente\*\* usando a tool `read\_file`:

&#x20;  - Para tabelas: `@/docs/table\_guideline.md` 

&#x20;  - Para funções: `@/docs/function\_guideline.md`

&#x20;  - Para APIs: `@/docs/api\_query\_guideline.md`

&#x20;  - Para tasks: `@/docs/task\_guideline.md`



2\. \*\*Revisar a seção de sintaxe relevante\*\* (ex: "Field Options" para campos de tabelas)



3\. \*\*Consultar os exemplos\*\* em `\*\_examples.md` quando houver dúvida



\*\*❌ NÃO FAÇA:\*\*

\- Criar arquivos .xs baseado apenas em conhecimento geral

\- Assumir sintaxe sem verificar a documentação

\- Ignorar as referências aos guidelines mencionadas nas instruções



\*\*✅ FAÇA:\*\*

\- `read\_file` do guideline específico

\- Verificar sintaxe de campos opcionais, defaults, filtros, etc.

\- Seguir os exemplos fornecidos



\*\*Exemplo do erro que isso previne:\*\*



// ❌ ERRADO (sem consultar docs)

text status {

&#x20; description = "Status"

}



// ✅ CORRETO (após ler table\_guideline.md)

text status?="pending" {

&#x20; description = "Status"

}





\## Customizações do EduTrack AI



\### Nomenclatura e Padrões

1\. \*\*Língua:\*\* Código e variáveis sempre em \*\*INGLÊS\*\*.

2\. \*\*Banco de Dados:\*\* Use `snake\_case` (ex: `academic\_tasks`, `user\_id`).

3\. \*\*Branches Git:\*\* Use prefixos `feat/`, `fix/`, `docs/` (ex: `feat/tabela-tarefas`).

4\. \*\*Commits:\*\* Siga Conventional Commits:

&#x20;  - `feat:` Nova funcionalidade

&#x20;  - `fix:` Correção de bug

&#x20;  - `docs:` Documentação

&#x20;  - `chore:` Manutenção



\### CHECKLIST de Validação OpenSpec (CRÍTICO)



> ⚠️ \*\*OBRIGATÓRIO: ANTES de criar qualquer proposal ou spec.md:\*\*

>

> \*\*VOCÊ DEVE usar `read\_file` para ler `openspec/AGENTS.md` COMPLETO.\*\*

>

> Este arquivo contém:

> - Estrutura obrigatória do `proposal.md` (## Why, ## What Changes, ## Impact)

> - Formatos de delta (## ADDED Requirements, ## MODIFIED Requirements, ## REMOVED Requirements)

> - Regras de formatação de scenarios (#### Scenario:)

> - Comandos de validação

>

> \*\*Sem ler este arquivo, você FALHARÁ na validação.\*\*



\*\*❌ Erros mais comuns que causam falha na validação:\*\*



1\. \*\*Localização do arquivo determina o formato\*\*

&#x20;  - ❌ Usar `## Requirements` em `openspec/changes/<id>/specs/capability/spec.md`

&#x20;  - ✅ Usar `## ADDED Requirements` em changes/ (são DELTAS, não specs finais)

&#x20;  - ✅ Usar `## Requirements` apenas em `openspec/specs/capability/spec.md` (specs permanentes)



2\. \*\*Hierarquia markdown incompleta\*\*

&#x20;  - ❌ Começar direto com `### Requirement:`

&#x20;  - ✅ Sempre começar com `# <nome> Specification` → `## Purpose` → `## Requirements` (ou `## ADDED Requirements` se em changes/)



3\. \*\*Palavras-chave incorretas\*\*

&#x20;  - ❌ "must", "should", "may" (minúsculas)

&#x20;  - ✅ SHALL ou MUST (maiúsculas)



4\. \*\*Scenarios faltando ou mal formatados\*\*

&#x20;  - ❌ Requirement sem scenario

&#x20;  - ❌ Scenario em texto corrido

&#x20;  - ✅ Todo requirement TEM ≥1 scenario com bullets \*\*WHEN\*\*/\*\*THEN\*\*



\*\*Estrutura para arquivos em openspec/changes/<id>/specs/capability/spec.md:\*\*



&#x20;   # capability-name Specification

&#x20;   

&#x20;   ## Purpose

&#x20;   \[O que é e por quê]

&#x20;   

&#x20;   ## ADDED Requirements    ← IMPORTANTE: Use ADDED (não apenas Requirements)

&#x20;   

&#x20;   ### Requirement: Fazer X

&#x20;   Sistema SHALL fazer X.

&#x20;   

&#x20;   #### Scenario: Caso de uso

&#x20;   - \*\*WHEN\*\* condição

&#x20;   - \*\*THEN\*\* resultado



\### Conhecimento do Schema

1\. \*\*Tabela Existente:\*\* `users` já existe no Xano.

2\. \*\*Relacionamentos:\*\* Sempre use `user\_id` para vincular ao usuário logado.



\### Segurança e Boas Práticas

1\. \*\*Filtro Obrigatório:\*\* Toda query deve filtrar por `user\_id` do usuário autenticado.

2\. \*\*APIs REST:\*\* Siga padrão RESTful:

&#x20;  - GET `/subjects` - Lista

&#x20;  - POST `/subjects` - Criar

&#x20;  - PATCH `/subjects/{id}` - Atualizar

&#x20;  - DELETE `/subjects/{id}` - Deletar

3\. \*\*Python:\*\* Use tratamento de erros (try/except) em lógica complexa.



\### Comunicação

1\. Explique o que vai fazer ANTES de fazer.

2\. Indique onde os arquivos serão criados/modificados.

3\. Pergunte se há dúvidas sobre as regras específicas deste projeto.



\## Exemplo de spec.md Válido



&#x20;   # subjects Specification

&#x20;   

&#x20;   ## Purpose

&#x20;   Define the database structure for managing academic subjects in EduTrack AI.

&#x20;   

&#x20;   ## Requirements

&#x20;   

&#x20;   ### Requirement: Create subjects table

&#x20;   The system SHALL store subject information for each user.

&#x20;   

&#x20;   #### Scenario: User creates a new subject

&#x20;   - \*\*WHEN\*\* user creates a new subject

&#x20;   - \*\*THEN\*\* system stores it with user\_id association



\## ⚠️ Estrutura INCORRETA (Falha na Validação)



&#x20;   ### Requirement: Create subjects table

&#x20;   \[conteúdo...]



\*\*Por quê falha:\*\* Começa no nível 3 (###) sem o título principal (#), ## Purpose e ## Requirements.