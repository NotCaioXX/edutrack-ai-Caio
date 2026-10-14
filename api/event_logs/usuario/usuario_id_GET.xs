// Get usuario record
query "usuario/{usuario_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int usuario_id? filters=min:1
  }

  stack {
    db.get usuario {
      field_name = "id"
      field_value = $input.usuario_id
    } as $usuario
  
    precondition ($usuario != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $usuario
  guid = "pDFLyuff5zlvSrdYgU614Nh9NI4"
}