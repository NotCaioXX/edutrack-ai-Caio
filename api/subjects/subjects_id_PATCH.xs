// Update an academic subject
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subjects_id filters=min:1
    text name? filters=trim
    text teacher? filters=trim
    int hours? filters=min:0
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

    db.edit subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = {
        name   : $input.name
        teacher: $input.teacher
        hours  : $input.hours
      }
    } as $updated_subject
  }

  response = $updated_subject
  guid = "2YQZU7yinvnw4CeZRrjuMz6gHCg"
}

