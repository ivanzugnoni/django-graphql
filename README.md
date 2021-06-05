# django-graphql

Sample project of a Django API using GraphQL


### Setup

Install dependencies using [Poetry](https://python-poetry.org/docs/)
```
$ poetry install
```

Run Django migrations (make sure to have `PYTHONPATH` and `DJANGO_SETTINGS_MODULE` envvars properly set)
```
$ django-admin migrate
```

Load initial data
```
$ django-admin loaddata django_graphql/library/initial_data.json
```