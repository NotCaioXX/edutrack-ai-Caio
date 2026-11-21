# top-navbar-navigation Specification

## Purpose

Define a barra superior de navegação (navbar/header) em substituição à barra lateral, a ordenação das páginas 3 (Progresso) e 4 (Perfil), a limpeza visual da Página Inicial, a tradução dos menus dropdown de status, a remoção de referências textuais a tabelas do Xano na interface, a substituição dos emojis pelos logos customizados das páginas e do projeto (com ampliação de 3x, logo home e logo perfil na navbar), o tema escuro com fundo preto `#000000`, a estilização do calendário da Página Inicial e a remoção completa de emojis em todas as páginas mantendo apenas as logos existentes.

## ADDED Requirements

### Requirement: Barra superior de navegação (navbar/header)
The system SHALL hide the default Streamlit sidebar page navigation list and display a top navigation bar (navbar/header) across all application pages with links to all available pages.

#### Scenario: User navigates using the top navbar
- **WHEN** the user clicks on any page link in the top navigation bar
- **THEN** the system redirects to the selected page while keeping the top navigation accessible

#### Scenario: Sidebar page list remains hidden
- **WHEN** any page of the application is rendered
- **THEN** the default Streamlit sidebar page navigation (`stSidebarNav`) SHALL be hidden from view

### Requirement: Ordenação e links das páginas 3 e 4
The system SHALL designate Progresso as page 3 and Perfil as page 4, updating all internal page links and references accordingly.

#### Scenario: Navigation links target Progresso as page 3 and Perfil as page 4
- **WHEN** links to Progresso or Perfil are rendered or activated
- **THEN** Progresso targets `pages/3_📊_Progresso.py` and Perfil targets `pages/4_👤_Perfil.py`

### Requirement: Limpeza visual da Página Inicial
The system SHALL remove the direct login/profile shortcut button, the redundant title header with caption, and the "Acesso Rápido" section from `Página Inicial.py`.

#### Scenario: Home page header does not contain login shortcut button
- **WHEN** the user visits the home page (`Página Inicial.py`)
- **THEN** the header displays the title without an individual shortcut button to the login page

#### Scenario: Home page does not display redundant title header
- **WHEN** the user views the top section of `Página Inicial.py` below the navbar
- **THEN** the page displays the metric cards directly without a redundant title header or login caption

#### Scenario: Home page does not display Acesso Rápido section
- **WHEN** the user scrolls to the bottom of the home page (`Página Inicial.py`)
- **THEN** the "Acesso Rápido" section is not displayed

### Requirement: Tradução dos menus dropdown de status
The system SHALL display all task status dropdowns with translated Portuguese labels: "Pendente", "Em progresso", and "Concluído", while preserving the underlying database values.

#### Scenario: Status options in dropdowns are displayed in Portuguese
- **WHEN** the user views or selects a status filter or task status in any dropdown
- **THEN** the options displayed are "Pendente", "Em progresso", and "Concluído" (with "Todos" available in filters)

### Requirement: Remoção de referências textuais a tabelas do Xano
The system SHALL remove technical database table references (such as `(Tabela subjects)` and `(Tabela academic_tasks)`) from user-facing metric labels and section subheaders across all pages.

#### Scenario: User views metric cards and subheaders without table names
- **WHEN** the user views dashboard metrics or form subheaders
- **THEN** labels display plain descriptions without technical table identifiers

### Requirement: Substituição de emojis por logos customizados
The system SHALL replace emoji icons for Início, Disciplinas, Tarefas, and Progresso with their respective logo images from `assets/logos/`, enlarge the project brand logo by 3x, and display `prog_00000.png` next to the progress overview section on the home page.

#### Scenario: Top navbar renders custom logos for pages
- **WHEN** the top navigation bar is displayed
- **THEN** navigation links for Início, Disciplinas, Tarefas, and Progresso display their respective logo icons (`home`, `disci`, `tarefa`, `prog`) instead of emojis

#### Scenario: Main page title header displays custom logo
- **WHEN** the user visits Disciplinas, Tarefas, or Progresso
- **THEN** the main page header displays the custom logo image next to the page title

#### Scenario: Brand title renders project logo enlarged by 3x
- **WHEN** the top navigation bar is displayed
- **THEN** the brand displays the official project logo image (`logo_00000.png`) scaled 3x (`5.1rem`) with vertically centered alignment

#### Scenario: Progress overview section on home page displays prog logo
- **WHEN** the user views the progress overview section on the home page
- **THEN** the section header displays the `prog_00000.png` logo instead of an emoji

### Requirement: Fundo preto para o modo escuro
The system SHALL configure the dark theme background color to pure black (`#000000`) for the application.

#### Scenario: Dark mode renders with black background
- **WHEN** the application is loaded
- **THEN** the theme background color is configured as `#000000`

### Requirement: Estilização do calendário da Página Inicial
The system SHALL display the home page calendar card with gray background and border, render today's date marker as a filled blue circle, and render pending task dates as filled red circles (`#ff0000`).

#### Scenario: Calendar displays with gray background
- **WHEN** the user views the calendar on the home page
- **THEN** the calendar container and elements SHALL render with a dark gray background and border

#### Scenario: Today's date marker is filled in blue
- **WHEN** the user views the current day on the home page calendar
- **THEN** the date number SHALL be enclosed within a filled blue circle with white text

#### Scenario: Pending tasks dates are filled in red
- **WHEN** any day with pending tasks is rendered on the home page calendar
- **THEN** the day number SHALL be enclosed within a filled red circle (`#ff0000`) with white text

### Requirement: Logo de Perfil na barra de navegação
The system SHALL display the custom profile logo image (`perfil_00000.png`) for the Perfil link in the top navigation bar instead of an emoji.

#### Scenario: Top navbar renders custom profile logo
- **WHEN** the top navigation bar is displayed
- **THEN** the Perfil navigation link displays the custom logo image (`perfil_00000.png`)

### Requirement: Remoção de emojis em todas as páginas
The system SHALL remove all emoji characters across all application pages, keeping only custom graphic logos where they already exist.

#### Scenario: Pages render without emoji characters
- **WHEN** any page of the application is viewed
- **THEN** textual elements and action controls SHALL not contain emoji characters and only predefined graphic logos remain visible
