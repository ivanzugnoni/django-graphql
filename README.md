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
$ django-admin loaddata initial_data.json
```

Runserver
```
$ django-admin runserver
```

Accessing to `localhost:8000/graphql` in your web browser will allow you to start using the GraphQL playground and perform some queries 🎉


### Examples

##### --> Query with Filtering, Ordering and Nested nodes

<img src="https://user-images.githubusercontent.com/2788551/120910239-a6ebf980-c653-11eb-8466-bdcabb20ee4f.png" width="75%">

##### --> Mutations (create - update - delete)

<img src="https://user-images.githubusercontent.com/2788551/120910959-70b17880-c659-11eb-952d-ca96f03e7083.png" width="75%">

<img src="https://user-images.githubusercontent.com/2788551/120910976-9a6a9f80-c659-11eb-9c5a-7aa6dfc8bf56.png" width="75%">

<img src="https://user-images.githubusercontent.com/2788551/120910990-b3735080-c659-11eb-8b79-106e36040b26.png" width="75%">
