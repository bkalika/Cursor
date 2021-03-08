Build docker images
$ uid=$(id -u) gid=$(id -g) docker-compose build


Start compose
$ uid=$(id -u) gid=$(id -g) docker-compose up


Connect to the container
$ uid=$(id -u) gid=$(id -g) docker exec -ti concierge_app_1 bash


Load fixtures from file (in container)
# concierge/manage.py loaddata --format=json concierge/fixtures/staff_initial_data.json


Collect staticfiles
# concierge/manage.py collectstatic --noinput


Create super user
# concierge/manage.py createsuperuser


Apply migrations
# concierge/manage.py migrate


# get user's model
>>>from django.contrib.auth import get_user_model

# bulk creation
>>> User.objects.bulk_create([User(username='test_bulk_1'), User(username='test_bulk_2')])