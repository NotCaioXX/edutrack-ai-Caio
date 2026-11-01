// Query all usuario records
query usuario verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $usuario
  }

  response = $usuario
  guid = "iRJkLU5oaHop-NEAFjFvrT9Txtc"
}