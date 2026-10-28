// Create a new academic task
query "academic_tasks" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int subject_id filters=min:1
    text title filters=trim
    text description? filters=trim
    date due_date?
    text status?="pending" filters=trim
  }

  stack {
    precondition ($input.title != "") {
      error_type = "badrequest"
      error = "Task title is required."
    }

    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $linked_subject

    precondition ($linked_subject != null && $linked_subject.user_id == $auth.id) {
      error_type = "badrequest"
      error = "Subject not found or does not belong to the user."
    }

    db.add academic_tasks {
      data = {
        created_at : "now"
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
      }
    } as $task
  }

  response = $task
  guid = "Fkv0r2NBNuAQHS1xvoN8nMdiEgU"
}

