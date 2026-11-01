// Stores student obligations and tasks linked to subjects
table academic_tasks {
  auth = false

  schema {
    // Unique identifier for the task
    // Unique identifier for the task
    int id
  
    // Creation timestamp
    // Creation timestamp
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // Reference to the authenticated user / student
    // ID of the student who owns the task
    int user_id {
      table = "user"
    }
  
    // Reference to the academic subject
    // ID of the subject this task belongs to
    int subject_id {
      table = "subjects"
    }
  
    // Title / headline of the task
    // Title of the task
    text title filters=trim
  
    // Detailed description or instructions for the task
    // Detailed task description
    text description? filters=trim
  
    // Target completion or deadline date
    // Due date for the task
    date due_date?
  
    // Current lifecycle status (e.g., pending, in_progress, completed)
    // Task status
    text status?=pending filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]

  guid = "AIf_Roi9Z31NHsxlc9HQ7hSFNyQ"
}