// Stores student obligations and tasks linked to subjects
table academic_tasks {
  auth = false

  schema {
    // Unique identifier for the task
    int id {
      description = "Unique identifier for the task"
    }

    // Creation timestamp
    timestamp created_at?=now {
      visibility = "private"
      description = "Creation timestamp"
    }

    // Reference to the authenticated user / student
    int user_id {
      table = "user"
      description = "ID of the student who owns the task"
    }

    // Reference to the academic subject
    int subject_id {
      table = "subjects"
      description = "ID of the subject this task belongs to"
    }

    // Title / headline of the task
    text title filters=trim {
      description = "Title of the task"
    }

    // Detailed description or instructions for the task
    text description? filters=trim {
      description = "Detailed task description"
    }

    // Target completion or deadline date
    date due_date? {
      description = "Due date for the task"
    }

    // Current lifecycle status (e.g., pending, in_progress, completed)
    text status?="pending" filters=trim {
      description = "Task status"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]
  guid = "AIf_Roi9Z31NHsxlc9HQ7hSFNyQ"
}