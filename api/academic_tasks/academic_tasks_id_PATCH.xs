// Update an academic task
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int academic_tasks_id filters=min:1
    int subject_id?
    text title? filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
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

    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = {
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
      }
    } as $updated_task
  }

  response = $updated_task
  guid = "bkQRlLgnwv3hxSc6mPNRxLlRyEE"
}

