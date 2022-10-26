## Fastapi access system
____
This library provides a tool to perform access control over endpoints
```python
from fastapi import FastAPI, Depends

from fastapi_access import AccessControl, Rule

def get_current_user():
    return {
        'username': 'test',
        'job': 'storekeeper',
        'roles': [
            {'slug': 'admin', 'name': 'some_admin_name'},
            {'slug': 'staff', 'name': 'some_staff_name'}
        ]
    }

app = FastAPI()
AccessControl.set_access_data_func(app, get_current_user)

@app.get('/path', dependencies=[Depends(AccessControl(
    (Rule('username') == 'test')
    & (Rule('job') == 'storekeeper')
))])
def hello_world():
    return {'message': 'Hello World!'}
```

____
Setting source for getting information

Allowed to use Fastapi Dependency stack
```python
AccessControl.set_access_data_func(app, get_current_user)
```
____
Supported operation types

| Name                   | Syntax                                                 |
|------------------------|--------------------------------------------------------|
| EQUAL:                 | `Rule('username') == 'test'  `                         |
| NOT_EQUAL:             | `Rule('username') != 'test' `                          |
| GREATE                 | `Rule('age') > 25   `                                  |
| LOWER                  | `Rule('age') < 25`                                     |
| GREATER <br/> or EQUAL | `Rule('age') >= 25`                                    |
| LOWER <br/> or EQUAL   | `Rule('age') <= 25`                                    |
 | CONTAINS               | `Rule('roles').contains('staff')`                      |
 | NOT_CONTAINS           | `Rule('roles').not_contains('staff')`                  |
| IN                     | `Rule('organization_id').in_([3,4,5])`                 |
 | NOT_ID                 | `Rule('organization_id').not_in_([3,4,5]) `            |
 | AND                    | `Rule('is_superuser') & (Rule('username') == 'admin')` |
 | OR                     | `Rule('is_superuser') \| Rule('username') == 'admin'`  |
----
You can combine rules as you wish
```python
from fastapi_access import Rule

rules = (
    Rule('is_superuser')
    | (Rule('username') == 'admin')
    | Rule('roles').contains('admin')
    | (
        (Rule('organization_id') == 5)
        & Rule('roles', 'slug').contains('staff')
    )
)
```
