# ToDo API
```
/api/auth/users/ POST registration
/api/auth/users/me/ GET user info
/api/auth/token/login/ POST login
/api/auth/token/logout/ POST logout
/api/groups/ GET list of groups
/api/groups/ POST create group (group_description)
/api/groups/{group_id}/ PUT change group info
/api/groups/{group_id}/ DELETE delete group
/api/todos/?group_id={group_id} GET list of todos
/api/todos/ POST create todo (send group_id in JSON)
/api/todos/{todo_id}/ GET get exact todo
/api/todos/{todo_id}/ PUT change todo
/api/todos/{todo_id}/ DELETE delete todo
/api/groups-member/ POST join to group
/api/groups-member/?group_id={group_id} GET group members usernames
/api/groups-member/{group_id}/ PUT change smth
/api/groups-member/{group_id}/ DELETE delete member from group
```