# Tasks

## 1. Backend CRUD Endpoints - Subjects

- [x] 1.1 Criar/verificar endpoints CRUD de `subjects` (`GET /subjects`, `POST /subjects`, `GET /subjects/{id}`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`) em `api/subjects/` com isolamento por `$auth.id`

## 2. Backend CRUD Endpoints - Academic Tasks

- [x] 2.1 Criar/verificar endpoints CRUD de `academic_tasks` (`GET /academic_tasks`, `POST /academic_tasks`, `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`) em `api/academic_tasks/` com isolamento por `$auth.id`

## 3. Integração Frontend - Disciplinas

- [x] 3.1 Integrar `pages/1_📚_Disciplinas.py` para buscar dados (`GET /subjects`) e salvar/remover disciplinas (`POST /subjects`, `DELETE /subjects/{id}`) no Xano usando o token de autenticação

## 4. Integração Frontend - Tarefas

- [x] 4.1 Integrar `pages/2_📝_Tarefas.py` para buscar dados (`GET /academic_tasks`) e salvar/atualizar/remover tarefas (`POST /academic_tasks`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`) no Xano usando o token de autenticação
