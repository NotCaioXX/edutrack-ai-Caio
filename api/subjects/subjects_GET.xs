// List subjects belonging to the authenticated user
query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  guid = "18RZC7lVzrtw-Qn_WAjlx2cZ-ow"
}