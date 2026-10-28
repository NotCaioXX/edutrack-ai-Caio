// Tabela de disciplinas acadêmicas dos usuários
table subjects {
  auth = false

  schema {
    // Identificador único da disciplina
    int id
  
    // Nome da disciplina
    text name filters=trim
  
    // Nome do professor(a) responsável
    text teacher? filters=trim
  
    // Carga horária da disciplina em horas
    int hours? filters=min:0
  
    // Identificador do usuário proprietário da disciplina
    int user_id {
      table = "user"
    }
  
    // Data e hora de criação do registro
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]

  guid = "nvDqFMZ566mWz7QEF-iYTVzqsYI"
}