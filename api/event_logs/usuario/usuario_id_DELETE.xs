// Delete usuario record.
query "usuario/{usuario_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int usuario_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.usuario_id
    }
  }

  response = null
  guid = "CMVv9Plovu9-fQuitCPbu-qT2Ic"
}