// Create a new academic subject
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text teacher? filters=trim
    int hours? filters=min:0
  }

  stack {
    precondition ($input.name != "") {
      error_type = "badrequest"
      error = "Subject name is required."
    }
  
    db.add subjects {
      data = {
        created_at: "now"
        user_id   : $auth.id
        name      : $input.name
        teacher   : $input.teacher
        hours     : $input.hours
      }
    } as $subject
  }

  response = $subject
  guid = "ABJhwjnDzAtcPKiQoko8ZHsLDNM"
}