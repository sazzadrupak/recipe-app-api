# recipe-app-api
Recipe app API source code

### start project
    ```docker-compose run app sh -c "django-admin.py startproject app ."```

### run tests
    ```docker-compose run app sh -c "python manage.py test && flake8"```
    N.B. Before run that command, please build the docker-compose to update the package dependencies with following command
    ```docker-compose build```
    
### create an app
    ```docker-compose run app sh -c "python manage.py startapp core"```


### run an migration in a app
    ```docker-compose run app sh -c "python manage.py makemigrations core"```
    N.B. It is better to add app name of which the migration belongs to
    
### create a super user
    ```docker-compose run app sh -c "python manage.py createsuperuser"```