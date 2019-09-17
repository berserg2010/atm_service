## ATM Service

### BACKEND

#### INSTALL

##### DEBIAN

>###### FOLDER STRUCTURE
>
>```
>atm_service/
>   backend/
>```


From _python3_:

\# `apt install python3-virtualenv python3-pip python3-dev virtualenv`

In `atm_service/backend/`:

\$ 

\$ `virtualenv --prompt="(venv:atm_service)" -p /usr/bin/python3 ./venv/`

\$ `source ./venv/bin/activate`

\$ `pip3 install -U -r requirements.txt`

\$ `django-admin.py startproject backend`

\$ `cd backend/`

\$ `python3 manage.py startapp api`


***

#### TESTING

To run the tests, you must run in a virtual environment:

`pytest`


***
