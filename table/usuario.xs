// usuario do pograma legal
table usuario {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text cunty? filters=trim
    email email? filters=trim|lower
    text nome? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "fd_Oeb0juu6rk2-72m8S06n6_vY"
}