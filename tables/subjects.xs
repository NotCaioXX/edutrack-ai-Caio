// Academic subjects/courses tracked by students
table subjects {
  auth = false

  schema {
    // Unique identifier for the subject
    int id {
      description = "Unique identifier for the subject"
    }

    // Creation timestamp
    timestamp created_at?=now {
      visibility = "private"
      description = "Creation timestamp"
    }

    // ID of the authenticated user
    int user_id {
      table = "user"
      description = "ID of the authenticated user"
    }

    // Subject title / course name
    text name filters=trim {
      description = "Subject title / course name"
    }

    // Name of the teacher or instructor
    text teacher? filters=trim {
      description = "Name of the teacher or instructor"
    }

    // Total course workload in hours
    int hours? filters=min:0 {
      description = "Total course workload in hours"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
}

