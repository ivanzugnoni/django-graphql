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

Runserver
```
$ django-admin runserver
```

Accessing to `localhost:8000/graphql` in your web browser will allow you to start using the GraphQL playground and perform some queries 🎉


### Examples

##### Query with Filtering, Ordering and Nested nodes

![image](https://user-images.githubusercontent.com/2788551/120910239-a6ebf980-c653-11eb-8466-bdcabb20ee4f.png)

