// Retrieve a specific academic task by id
query "academic_tasks/{academic_tasks_id}" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id filters=min:1
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $existing_task
  
    precondition ($existing_task != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    precondition ($existing_task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  }

  response = $existing_task
  guid = "bu3m7GW7VCZ4FZ1MmpJY14TxsWw"
}