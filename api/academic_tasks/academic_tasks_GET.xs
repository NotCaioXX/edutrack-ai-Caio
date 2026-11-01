// List academic tasks belonging to the authenticated user
query academic_tasks verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
  }

  stack {
    db.query academic_tasks {
      where = $db.user_id == $auth.id
      return = {type: "list"}
    } as $tasks
  }

  response = $tasks
  guid = "yadOFe--Ybq9EgvwLO0NyS9Pbc8"
}