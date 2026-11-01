// Delete an academic subject
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $existing_subject
  
    precondition ($existing_subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($existing_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  
    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = {success: true}
  guid = "-7rpQFtwdYzJkSD-aLuzNqLP57A"
}