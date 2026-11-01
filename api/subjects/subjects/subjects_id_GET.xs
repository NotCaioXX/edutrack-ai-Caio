// Retrieve a specific academic subject by id
query "subjects/{subjects_id}" verb=GET {
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
  }

  response = $existing_subject
  guid = "uXZTdPyJmIlMIE905OPt_aDAEWw"
}