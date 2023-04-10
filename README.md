# Form Catcher <!-- omit in toc -->

A simple API to collect form submissions and send the contents to a specific
Email address. Users can define a site with an email address and receive a
unique slug in return. This slug will be used in the client Form `action` to get
the correct email address to send the Form data. The API will take arbitrary
form fields, the user does not need to set them in advance.

This is currently just a Work in progress and not properly secured. It does
accept and decode form submissions and send this data to the specified site
email, but there is no Authentication/Authorization so should not be used as a
production tool just yet.

There is also (currently) no User Authentication or Authorization so sites can
be added or deleted by anyone, this will be fixed shortly.

- [Setup](#setup)
  - [Configuration](#configuration)
  - [Set up a Virtual Environment](#set-up-a-virtual-environment)
  - [Install required Dependencies](#install-required-dependencies)
  - [Migrate the Database](#migrate-the-database)
- [Run the API](#run-the-api)
- [API Routes](#api-routes)
  - [**`GET`** _/_](#get-)
  - [**`GET`** _/form/{slug}_](#get-formslug)
  - [**`POST`** _/form/{slug}_](#post-formslug)
  - [**`GET`** _/site/_](#get-site)
  - [**`POST`** _/site/_](#post-site)
  - [**`GET`** _/site/{slug}_](#get-siteslug)
  - [**`DELETE`** _/site/{slug}_](#delete-siteslug)

## Setup

### Configuration

Database (and other) settings can be read from environment variables or from a
`.env` file in the project root. By default, these are only used for the
Database and Email setup.

```ini
# The Base API Url. This is where your API wil be served from, and can be read
# in the application code. It has no effect on the running of the applciation
# but is an easy way to build a path for API responses. Defaults to
# http://localhost:8000
BASE_URL=http://localhost:8000

# Database Settings - These must be changed to match your setup.
DB_USER=dbuser
DB_PASSWORD=my_secret_passw0rd
DB_ADDRESS=localhost
DB_PORT=5432
DB_NAME=my_database_name

# Email Settings
MAIL_USERNAME=emailuser
MAIL_PASSWORD=12345!
MAIL_FROM=myemail@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.mailserver.com
MAIL_FROM_NAME="Form Catcher by Seapagan"
```

### Set up a Virtual Environment

It is always a good idea to set up dedicated Virtual Environment when you are
developing a Python application. If you use Poetry, this will be done
automatically for you when you run `poetry install`.

Otherwise, [Pyenv](https://github.com/pyenv/pyenv) has a
[virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin which is very
easy to use.

Also, check out this
[freeCodeCamp](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
tutorial or a similar
[RealPython](https://realpython.com/python-virtual-environments-a-primer/) one
for some great info. If you are going this (oldschool!) way, I'd recommend using
[Virtualenv](https://virtualenv.pypa.io/en/latest/) instead of the built in
`venv` tool (which is a subset of this).

### Install required Dependencies

The project has been set up using [Poetry](https://python-poetry.org/) to
organize and install dependencies. If you have Poetry installed, simply run the
following to install all that is needed.

```console
poetry install
```

You now need to activate the VirtualEnv:

```console
poetry shell
```

### Migrate the Database

Make sure you have [configured](#configuration) the database. Then run the
following command to setup the database:

```console
alembic upgrade head
```

Everytime you add or edit a model, create a new migration then run the upgrade
as shown below:

```console
alembic revision -m "<My commit message>"
alembic upgrade head
```

Check out the [Alembic](https://github.com/sqlalchemy/alembic) repository for
more information on how to use (for example how to revert migrations).

## Run the API

```terminal
uvicorn form_catch.main:app --reload
```

## API Routes

<!-- openapi-schema -->

### **`GET`** _/_

> Root : _Root endpoint to check if the API is running successfully._

### **`GET`** _/form/{slug}_

> Respond To Form : _Get the supplied form data and email it._
>
> Note that the slug is used to determine the email address to send the form
> data to.
>
> Also, this route responds to both GET and POST requests.
>
### **`POST`** _/form/{slug}_

> Respond To Form : _Get the supplied form data and email it._
>
> Note that the slug is used to determine the email address to send the form
> data to.
>
> Also, this route responds to both GET and POST requests.

### **`GET`** _/site/_

> Get Sites : _Get all sites._
>
### **`POST`** _/site/_

> Create Site : _Create a new site._

### **`GET`** _/site/{slug}_

> Get Site : _Get a site by its slug._
>
### **`DELETE`** _/site/{slug}_

> Delete Site : _Delete a site by its slug._
<!-- openapi-schema-end -->
