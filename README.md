# Form Catcher <!-- omit in toc -->

A simple API to collect form submissions and send the contents to a specific
Email address. Users can define a site with an email address and receive a
unique slug in return. This slug will be used in the client Form `action` to get
the correct email address to send the Form data. The API will take arbitrary
form fields, the user does not need to set them in advance.

This is currently just a Work in progress and not properly secured. It does
accept and decode form submissions and send this data to the specified site
email, but there is no Authentication/Authorization so should not be used as a
production tool just yet (**anyone** can add/edit/delete sites!).

- [Setup](#setup)
  - [Configuration](#configuration)
    - [Lockdown Mode](#lockdown-mode)
  - [Set up a Virtual Environment](#set-up-a-virtual-environment)
  - [Install required Dependencies](#install-required-dependencies)
  - [Migrate the Database](#migrate-the-database)
- [Run the API](#run-the-api)
- [Usage](#usage)
  - [Create a Site](#create-a-site)
  - [Create your Form](#create-your-form)
  - [Check your Email](#check-your-email)
- [Demo site](#demo-site)
- [API Routes](#api-routes)
  - [**`GET`** _/_](#get-)
  - [**`GET`** _/form/echo_](#get-formecho)
  - [**`POST`** _/form/echo_](#post-formecho)
  - [**`GET`** _/form/{slug}_](#get-formslug)
  - [**`POST`** _/form/{slug}_](#post-formslug)
  - [**`GET`** _/site/_](#get-site)
  - [**`POST`** _/site/_](#post-site)
  - [**`GET`** _/site/{slug}_](#get-siteslug)
  - [**`DELETE`** _/site/{slug}_](#delete-siteslug)

## Setup

### Configuration

Database (and other) settings can be read from environment variables or from a
`.env` file in the `form_catch` subdirectory.

```ini
# The Base API Url. This is where your API wil be served from, and can be read
# in the application code. It has no effect on the running of the application
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

# Lockdown the API - This will prevent any new sites from being created, or
# existing sites edited/deleted. This is useful if you want to prevent
# accidental changes to the API. Defaults to False
LOCKDOWN=False
```

#### Lockdown Mode

Once you have set up your site(s) it can be advantageous to block anyone else
from creating or editing (or more importantly) deleting the site(s).

For this there is the `LOCKDOWN` environment variable. Set this in the  `.env`
file as above.

```ini
LOCKDOWN=False # default, API is open
```

or

```ini
LOCKDOWN=True # all routes under '/site' are removed and blocked.
```

Unless you are operating a public service where people can add their own sites,
it is recommended to set `LOCKDOWN=True` for any public-facing catcher.

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
alembic revision --autogenerate -m "<My commit message>"
alembic upgrade head
```

Check out the [Alembic](https://github.com/sqlalchemy/alembic) repository for
more information on how to use (for example how to revert migrations).

## Run the API

From your Poetry shell, run either

```terminal
poe serve
```

or

```terminal
poetry poe serve
```

(the latter also works outside the Poetry shell)

This is the equivalent of running `uvicorn form_catch.main:app --reload` from
inside the Poetry shell

**Important** - this is only useful during development mode! For a production
server, use one of the secure methods noted in the [FastAPI
Documentation](https://fastapi.tiangolo.com/deployment/)

## Usage

### Create a Site

First you need to Create a Site. This just links a unique slug address to your
email address, with some configuration options.

Send a POST request to the `/site` URL with the following Body content:

```json
{
  "name": "My Site",
  "email": "my_email@google.com",
  "redirect_url": "https://mysite.com/submitted.html"
}
```

Where '_name_' is the friendly name for your site, '_email_' is the address that
form data should be sent to and '_redirect_url_' is the URL to redirect to after
the form is submitted.

On submitting this, you will recieve a 'slug' parameter back, which should be
used in your HTML forms. You will also recive an 'action' parameter which
includes the full URL needed for your form.

```json
{
  "name": "My Site",
  "slug": "rNPf97Tg",
  "action": "https://www.myformresponder.com/form/rNPf97Tg"
}
```

### Create your Form

Once you have the site created, you can use this in your HTML forms as the
'action' in the format `<URL>/form/slug`. In fact, just copy the 'action' field
from the response above into the `action` parameter of the form. All form fields
are fluid and entirely up to you, the API will return all the fields sent to it
with no further configuration needed:

```html
<form method="GET" action="https://www.myformresponder.com/form/rNPf97Tg">
  <label for="first_name">First Name</label>
  <input type="text" name="first_name" id="first_name" />
  <label for="last_name">Last Name</label>
  <input type="text" name="last_name" id="last_name" />
  <label for="email">Email</label>
  <input type="email" name="email" id="email" />
  <button type="submit">Submit</button>
</form>
```

Note that the `method=` can be either `GET` or `POST` as you desire, both will be
captured.

### Check your Email

All submissions will be sent to the email address you specified when creating
the site.

## Demo site

There is an example demo site in the [html_example](/html_example/) folder, load
the [formtest.html](/html_example/formtest.html) in a web browser to use it.

This tests both `GET` and `POST` form methods.

To use this you will need a locally running server [see above](#run-the-api),
with at least one site set up - change the `action=` parameter to match your own
site.

## API Routes

<!-- openapi-schema -->

### **`GET`** _/_

> Root : _Root endpoint to check if the API is running successfully._

### **`GET`** _/form/echo_

> Echo Form : _Echo the form data back to the user._
>
> This is useful during development to see what data is being sent to the
> server.
>
> Note that this route responds to both GET and POST requests.
>
### **`POST`** _/form/echo_

> Echo Form : _Echo the form data back to the user._
>
> This is useful during development to see what data is being sent to the
> server.
>
> Note that this route responds to both GET and POST requests.

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
