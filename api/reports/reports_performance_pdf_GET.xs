// Retrieve student academic performance data for report generation and download
query "reports/performance_pdf" verb=GET {
  api_group = "Reports"
  auth = "user"

  input {
  }

  stack {
    // Retrieve subjects belonging to the authenticated student
    db.query subjects {
      where = $db.user_id == $auth.id
      return = {type: "list"}
    } as $subjects

    // Retrieve tasks belonging to the authenticated student
    db.query academic_tasks {
      where = $db.user_id == $auth.id
      return = {type: "list"}
    } as $tasks
  }

  response = {
    user_id : $auth.id
    subjects: $subjects
    tasks   : $tasks
  }
  guid = "l9k95Xxdo9-HxoclKmvkMHBYxhI"
}

