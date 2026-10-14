// Add usuario record
query usuario verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "usuario"
    }
  }

  stack {
    db.add usuario {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $usuario
  }

  response = $usuario
  guid = "15weD8G4Bvb0j7hTOBsxVCR3Tv8"
}