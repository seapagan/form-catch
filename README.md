# Form Catcher <!-- omit in toc -->

A simple API to collect form submissions and send the contents to a specific
Email address. Users can define a site with an email address and receive a
unique slug in return. This slug will be used in the client Form `action` to get
the correct email address to send the Form data. The API will take arbitrary
form fields, the user does not need to set them in advance.

This is currently a Work in progress so some functionality is lacking, though
the main purpose of the API (catching form data) is fully functional.

- [Setup](#setup)
  - [Configuration](#configuration)
    - [Lockdown Mode](#lockdown-mode)
- [Development](#development)
  - [Set up a Virtual Environment](#set-up-a-virtual-environment)
  - [Install required Dependencies](#install-required-dependencies)
  - [Install Git Pre-Commit hooks](#install-git-pre-commit-hooks)
  - [Migrate the Database](#migrate-the-database)
  - [Add a user](#add-a-user)
- [Run a development server](#run-a-development-server)
- [Usage](#usage)
  - [Create a Site](#create-a-site)
  - [Create your Form](#create-your-form)
  - [Check your Email](#check-your-email)
- [Demo site](#demo-site)
- [Deploying to Production](#deploying-to-production)
- [API Routes](#api-routes)
  - [**`GET`** _/form/echo_](#get-formecho)
  - [**`POST`** _/form/echo_](#post-formecho)
  - [**`GET`** _/form/{slug}_](#get-formslug)
  - [**`POST`** _/form/{slug}_](#post-formslug)
  - [**`GET`** _/site/_](#get-site)
  - [**`POST`** _/site/_](#post-site)
  - [**`GET`** _/site/{slug}_](#get-siteslug)
  - [**`DELETE`** _/site/{slug}_](#delete-siteslug)
  - [**`POST`** _/register/_](#post-register)
  - [**`POST`** _/login/_](#post-login)
  - [**`POST`** _/refresh/_](#post-refresh)
  - [**`GET`** _/verify/_](#get-verify)
  - [**`GET`** _/users/_](#get-users)
  - [**`GET`** _/users/me_](#get-usersme)
  - [**`POST`** _/users/{user\_id}/make-admin_](#post-usersuser_idmake-admin)
  - [**`POST`** _/users/{user\_id}/password_](#post-usersuser_idpassword)
  - [**`POST`** _/users/{user\_id}/ban_](#post-usersuser_idban)
  - [**`POST`** _/users/{user\_id}/unban_](#post-usersuser_idunban)
  - [**`PUT`** _/users/{user\_id}_](#put-usersuser_id)
  - [**`DELETE`** _/users/{user\_id}_](#delete-usersuser_id)

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

# generate your own super secret key here, used by the JWT functions.
# 32 characters or longer, definately change the below!!
SECRET_KEY=123456

# List of origins that can access this API, separated by a comma, eg:
# CORS_ORIGINS=http://localhost,https://www.gnramsay.com
# If you want all origins to access (the default), use * or leave commented:
CORS_ORIGINS=*

```

For a **PUBLIC API** (unless its going through an API gateway!), set
`CORS_ORIGINS=*`, otherwise list the domains (**and ports**) required. If you
use an API gateway of some nature, that will probably need to be listed.

To generate a good secret key you can use the below command on any system with
Python installed:

```console
$ python -c "import secrets; print(secrets.token_hex(32))"
f0b34967fc29a9b19c583bb2c2d20d0f27adac671a6c9a0ad016c8ac0f5f425f

```

If the database is not configured or cannot be reached, the Application will
disable all routes, print an error to the console, and return a a 500 status
code with a clear JSON message for all routes. This saves the ugly default
"Internal Server Error" from being displayed.

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

## Development

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
$ poetry install
```

You now need to activate the VirtualEnv:

```console
$ poetry shell
```

### Install Git Pre-Commit hooks

This stage is **optional but recommended** (however it is compulsory if you are
submitting a **Pull Request**).

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

This will ensure that all code meets the required linting standard before being
committed.

### Migrate the Database

Make sure you have [configured](#configuration) the database. Then run the
following command to setup the database:

```console
$ ./api-admin db init
```

(this is the same as running `alembic upgrade head`, though it will downgrade to
the base structure and delete all data as well)

Everytime you add or edit a model, create a new migration as shown below. You
will be asked for a commit message. This will create and apply the migration in
the same step:

```console
$ ./api-admin db revision
Enter the commit message for the revision: Added email to the users model

  Generating ..._added_email_to_the_users_model.py ...  done
```

This is the same as running the below commands, it is provided for ease of use:

```console
alembic revision --autogenerate -m "Commit message"
alembic upgrade head
```

Check out the [Alembic](https://github.com/sqlalchemy/alembic) repository for
more information on how to use (for example how to revert migrations).

Look at the built-in help for more details :

```console
$ ./api-admin db --help
Usage: api-admin db [OPTIONS] COMMAND [ARGS]...

 Control the Database.

Options:
  --help          Show this message and exit.

Commands:
  drop            Drop all tables and reset the Database
  init            Re-Initialise the database using Alembic.
  revision        Create a new revision.
  upgrade         Apply the latest Database Migrations.
```

### Add a user

It is possible to add Users to the database using the API itself, but you cannot
create an Admin user this way, unless you already have an existing Admin user in
the database.

This template includes a command-line utility to create a new user and
optionally make them Admin at the same time:

```console
$ ./api-admin user create
```

You will be asked for the new user's email etc, and if this should be an
Admin user (default is to be a standard non-admin User). These values can be
added from the command line too, for automated use. See the built in help for
details :

```console
$ ./api-admin user create --help
Usage: api-admin user create [OPTIONS]

  Create a new user.

  Values are either taken from the command line options, or interactively for
  any that are missing.

Options:
  --email       -e      TEXT  The user's email address [required]
  --first_name  -f      TEXT  The user's first name [required]
  --last_name   -l      TEXT  The user's last name [required]
  --password    -p      TEXT  The user's password [required]
  --admin       -a            Make this user an Admin
  --help                 Show this message and exit.
```

Note that any user added manually this way will automatically be verified (no
need for the confirmation email which will not be sent anyway.)

## Run a development server

The [uvicorn](https://www.uvicorn.org/) ASGI server is automatically installed
when you install the project dependencies. This can be used for testing the API
during development. There is a built-in command to run this easily :

```console
$ ./api-admin serve
```

This will by default run the server on <http://localhost:8000>, and reload after
any change to the source code. You can add options to change this

```console
$ ./api-admin serve --help

Usage: api-admin serve [OPTIONS]

  Run a development server from the command line.

  This will auto-refresh on any changes to the source in real-time.

Options:
  --port   -p   INTEGER   Define the port to run the server on  [default: 8000]
  --host   -h   TEXT      Define the interface to run the server on.  [default:
                          localhost]
  --reload --no-reload    Enable auto-reload on code changes [default: True]
  --help                  Show this message and exit.
```

If you need more control, you can run `uvicorn` directly :

```console
uvicorn main:app --reload
```

The above command starts the server running on <http://localhost:8000>, and it
will automatically reload when it detects any changes as you develop.

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

To use this you will need a locally running server [see
above](#run-a-development-server), with at least one site set up - change the
`action=` parameter to match your own site.

## Deploying to Production

There are quite a few ways to deploy a FastAPI app to production. There is a
very good discussion about this on the FastAPI [Deployment
Guide](https://fastapi.tiangolo.com/deployment/) which covers using Uvicorn,
Gunicorn and Containers.

My Personal preference is to serve with Gunicorn, using uvicorn workers behind
an Nginx proxy, though this does require you having your own server. There is a
pretty decent tutorial on this at
[Vultr](https://www.vultr.com/docs/how-to-deploy-fastapi-applications-with-gunicorn-and-nginx-on-ubuntu-20-04/).
For deploying to AWS Lambda with API Gateway, there is a really excellent Medium
post (and it's followup)
[Here](https://medium.com/towards-data-science/fastapi-aws-robust-api-part-1-f67ae47390f9),
or for AWS Elastic Beanstalk there is a very comprehensive tutorial at
[testdriven.io](https://testdriven.io/blog/fastapi-elastic-beanstalk/)

> Remember:  you still need to set up a virtual environment, install all the
> dependencies, setup your `.env` file (or use Environment variables if your
> hosting provider uses these - for example Vercel or Heroku) and set up and
> migrate your Database, exactly the same as for Develpment as desctribed above.

## API Routes

<!-- openapi-schema -->

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

### **`POST`** _/register/_

> Register A New User : _Register a new User and return a JWT token plus a
> Refresh Token._
>
> The JWT token should be sent as a Bearer token for each access to a
> protected route. It will expire after 120 minutes.
>
> When the JWT expires, the Refresh Token can be sent using the '/refresh'
> endpoint to return a new JWT Token. The Refresh token will last 30 days, and
> cannot be refreshed.

### **`POST`** _/login/_

> Login An Existing User : _Login an existing User and return a JWT token plus a
> Refresh Token._
>
> The JWT token should be sent as a Bearer token for each access to a
> protected route. It will expire after 120 minutes.
>
> When the JWT expires, the Refresh Token can be sent using the '/refresh'
> endpoint to return a new JWT Token. The Refresh token will last 30 days, and
> cannot be refreshed.

### **`POST`** _/refresh/_

> Refresh An Expired Token : _Return a new JWT, given a valid Refresh token._
>
> The Refresh token will not be updated at this time, it will still expire 30
> days after original issue. At that time the User will need to login again.

### **`GET`** _/verify/_

> Verify : _Verify a new user._
>
> The code is sent to  new user by email, which must then be validated here.

### **`GET`** _/users/_

> Get Users : _Get all users or a specific user by their ID._
>
> To get a specific User data, the requesting user must match the user_id, or
> be an Admin.
>
> user_id is optional, and if omitted then all Users are returned. This is
> only allowed for Admins.

### **`GET`** _/users/me_

> Get My User Data : _Get the current user's data only._

### **`POST`** _/users/{user_id}/make-admin_

> Make Admin : _Make the User with this ID an Admin._

### **`POST`** _/users/{user_id}/password_

> Change Password : _Change the password for the specified user._
>
> Can only be done by an Admin, or the specific user that matches the user_id.

### **`POST`** _/users/{user_id}/ban_

> Ban User : _Ban the specific user Id._
>
> Admins only. The Admin cannot ban their own ID!

### **`POST`** _/users/{user_id}/unban_

> Unban User : _Ban the specific user Id._
>
> Admins only.

### **`PUT`** _/users/{user_id}_

> Edit User : _Update the specified User's data._
>
> Available for the specific requesting User, or an Admin.
>
### **`DELETE`** _/users/{user_id}_

> Delete User : _Delete the specified User by user_id._
>
> Admin only.
<!-- openapi-schema-end -->
