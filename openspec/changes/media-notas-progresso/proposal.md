# Proposal: Média de Notas na Página de Progresso e no Relatório PDF

## Why

Atualmente no EduTrack AI, as notas já podem ser cadastradas nas atividades concluídas, mas a página de Progresso (`pages/3_📊_Progresso.py`) e a exportação do relatório oficial em PDF (`scripts/generate_pdf_report.py`) contabilizam apenas quantidades de tarefas (total, concluídas, pendentes) e percentual de conclusão. Os estudantes necessitam visualizar o seu rendimento acadêmico consolidado (média geral das notas das tarefas e média por disciplina) na tela de progresso e no documento PDF exportado.

## What Changes

- **Cálculo de Média de Notas (`scripts/calculate_progress.py`)**:
  - Calcular a média aritmética das notas das atividades concluídas com nota atribuída para cada disciplina (`average_grade`) e o total de atividades avaliadas (`graded_tasks`).
- **Visualização na Página de Progresso (`pages/3_📊_Progresso.py`)**:
  - Adicionar card de métrica de Média Geral no Resumo Executivo.
  - Exibir a média de notas de cada matéria no Detalhamento por Disciplina (ex: `Média de Notas: X.X / 10.0` ou `Sem notas lançadas`).
- **Inclusão no Relatório Oficial em PDF (`scripts/generate_pdf_report.py`)**:
  - Adicionar card de Média Geral no Resumo Executivo do PDF.
  - Adicionar coluna de Média na tabela detalhada de disciplinas do PDF.

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `progress-calculation`: Atualizar os cálculos de progresso para incluir média de notas das atividades por matéria e geral, exibindo esses dados na interface de Progresso e no relatório em PDF.

## Impact

- **Frontend/Scripts**:
  - `scripts/calculate_progress.py`
  - `pages/3_📊_Progresso.py`
  - `scripts/generate_pdf_report.py`
- **Backend/Xano**: Nenhuma alteração em schemas de banco necessária (o campo `grade` já existe em `academic_tasks`).
