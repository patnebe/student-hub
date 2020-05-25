# STUDENT HUB

## Introduction

This is my final project for the Udacity Full Stack Developer Nanodegree. It is a clone of the Udacity knowledge hub platform where students can request support from technical mentors while working on their nanodegree projects. I chose this project because I wanted to understand the design decisions underlying the backend APIs that power real world applications.

Trello Board: https://trello.com/b/dnp5X41N/student-hub

<br>

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python). Python 3.7 is the recommended version for this project.

#### Virtual Enviornment

Working within a virtual environment is recommended whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Tech Stack/Key Dependencies

- PostgreSQL database

- Auth0 for Authentication and Authorization

- [Flask](http://flask.pocoo.org/), a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for creating and running schema migrations

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to interact with the database models.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS

<br/>

### Running the local development server

From `student-hub` directory first ensure you are working using your created virtual environment. Then navigate into the src directory by executing:

```bash
cd src
```

- now you should be within the "student-hub/src" directory

Create the development and test databases by running

```bash
createdb dev_knowledge_hub
createdb test_knowledge_hub
```

Next run the database migrations by executing the following commands:

```bash
 flask db upgrade
```

- Note: The migrations are applied to only the development database. The creation of tables within the test database is done programmatically during tests.

Finally run the server by executing:

```bash
flask run
```

- Now the server should be running at http://127.0.0.1:5000/

<br/>

## API Design and Documentation

### 1. MVP Requirements

These are the key user stories for this product are:

- An admin can create nanodegrees
- An admin can create projects for nanodegrees
- An admin can view a list of all students enrolled in a nanodegree
- A student can enroll in a nanodegree
- A student can request for technical assistance by asking a question on the platform
- A student can update a question which was previously posted by them
- A student can delete a question which was previously asked by them
- A user can get a list of all the questions which have been asked by students

### 2. Data Models

- There are five data models which power this product: Nanodegree, Project, Question, User, Answer. One to Many, and Many-to-many relationships exist between these models.
- They can be found in the `student-hub/src/app/models` directory

### 3. Role Based Access Control

Roles

- Admin
  - Permissions --- `create:nanodegree`, `create:project`, `get:nanodegree-students`
- Student
  - Permissions --- `create:question`, `update:question`, `delete:question`, `create:answer`, `update:question`, `delete:question`

### 4. Endpoints

#### `POST /api/v1/nanodegrees`

Creates a new nanodgree and returns the newly created nanodegree

- Payload JSON- {title: str, description: str}
- Response JSON - {
  success: bool, data: {
  id: int, title: str, description: str}
  }
- Success status code - 201
- Required permission - "create:nanodegree"
- Role - Admin

#### `GET /api/v1/nanodegrees`

Returns a list of nanodegrees

- Payload JSON - None
- Response JSON - None {
  success: bool, data: [
  {
  id: int, title: str, description: str}, {
  id: int, title: str, description: str}
  ]
  }
- Success status code - 200
- Required permission - None
- Role - None

#### `POST /api/v1/nanodegrees/id/projects`

Creates a projects for a given nanodegree

- Payload JSON - [{title: str}, {title: str}] where each object represents a project
- Response JSON - {success: bool, message: str}
- Success status code - 201
- Required permission - "create:project"
- Role - Admin

#### `GET /api/v1/nanodegrees/id/projects`

Returns a list of projects for a given nanodegree

- Payload JSON - None
- Response JSON - {success: bool, data: [{id: int, title: str, nanodegree_id: int}]}
- Required permission - None
- Success status code - 200
- Role - None

#### `GET /api/v1/nanodegrees/id/students`

Returns a paginated list of students enrolled in a given nanodegree

- Payload JSON - Optional {page?: int, students_per_page?: int}
- Response JSON - {success: bool, data: {nanodegree: str, students: [{id: int}, {id: int}], has_next_page: bool, next_page: int || None, has_previous_page: bool, previous_page: int || None}}
- Success status code - 200
- Required permission - "get:nanodegree-studetns"
- Role - Admin

#### `GET /api/v1/nanodegrees/id/enroll`

Enrolls the person making the request in a given nanodegree

- Payload JSON - None
- Response JSON - {success: bool, message: str}
- Success status code - 200
- Required permission - None
- Role - None

#### `POST /api/v1/questions`

Request technical support from a mentor by posting a question

- Payload JSON - {nanodegree_id: int, project_id: int, title: str, details: str, github_link: str || None}
- Response JSON - {success: bool, data: {title: str, id: int, nanodegree_id: int, project_id: int, asked_by: int}}
- Success status code - 201
- Required permission - "create:question"
- Role - Student

#### `GET /api/v1/questions`

Get a paginated list of all the questions on the platform

- Payload - Optional {page?: int, questions_per_page?: int}
- Response JSON - {success: bool, data: {questions: [{title: str, id: int, nanodegree_id: int, project_id: int, asked_by: int}], has_next_page: bool, next_page: int || None, has_previous_page: bool, previous_page: int || None}}
- Success status code - 200
- Required permission - None
- Role - None

#### `PATCH /api/v1/questions/id`

- Payload JSON - {title?: str, details?: str, github_link?: str || None}
- Response JSON - {success: bool, message: str, data: {title: str, id: int, nanodegree_id: int, project_id: int, asked_by: int}}
- Success status code - 200
- Required permission - "update:question" (\*\* Note that this request is fulfilled only if it was made by the original poster of the question)
- Role - Student

#### `DELETE /api/v1/questions/id`

- Payload JSON - None
- Response JSON - {success: bool, message: str}
- Success status code - 200
- Required permission - "delete:question" (\*\* Note that this request is fulfilled only if it was made by the original poster of the question)
- Role - Student

<br/>

## Testing

A couple things to note about the tests:

- An AUTH0 machine to machine application was setup to automate the process of getting the tokens to needed to test RBAC functionality
- The credentials are stored within a .env file which will be placed in the src folder i.e. the student-hub/src directory
- Here's what the env file should look like

```
TEST_DATABASE_NAME='test_knowledge_hub'
DEV_DATABASE_NAME='dev_knowledge_hub'
DATABASE_PASSWORD={your_postgres_password}
DATABASE_USERNAME={your_username}

#Pagination
QUESTIONS_PER_PAGE=10
STUDENTS_PER_PAGE=10

#Auth0 Login credentials (Create an Auth0 API with the permissions listed above. Remember to enable RBAC for this API)
AUTH0_TENANT_DOMAIN={your_auth0_tenant_domain}
AUTH0_API_AUDIENCE={your_api_audience}
AUTH0_ALGORITHMS={alorithms_setup_on_Auth0}

#Student (create a machine-to-machine application on your Auth0 API and assign the student level permissions to it)
TEST_STUDENT_CLIENT_ID="enter-yours"
TEST_STUDENT_CLIENT_SECRET="enter-yours"

#Admin (create a machine-to-machine application on your Auth0 API and assign the admin level permissions to it)
TEST_ADMIN_CLIENT_ID="enter-yours"
TEST_ADMIN_CLIENT_SECRET="enter-yours"
```

---

### Testing the flask app locally

Ensure the environment variables have been properly configured using the env file then from the `src/tests` directory, execute:

```bash
pytest API_tests.py datamodels_tests.py
```

---

### Testing the flask app hosted live on Heroku

Live Heroku Deployment: https://udacity-student-hub.herokuapp.com
<br/>

First obtain your access tokens by carrying out the following steps:

1. Ensure you're currently working in the virtual environment created above, all dependencies have been installed, and environment variables have been set within the env file
2. From the `student-hub/src/tests` directory, execute

```
python get_tokens.py
```

3. Check for a newly created tokens.txt file in the `student-hub/src/tests` directory.
4. The `student_token` and the `admin_token` should be present within a dictionary in the newly created tokens.txt file.
5. Export them to the terminal to make requests using curl or add them to authorization headers if you intend to test the API using Postman.

Next, refer to the API Documentation above for the request methods, required payloads, access control (roles expected for the bearer token sent with each request), and expected results associated with each endpoint.

_Sample requests_

```
curl --request POST \
  --url https://udacity-student-hub.herokuapp.com/api/v1/nanodegrees \
  --header "authorization: Bearer ${admin_token}" \
  --header "Content-Type: application/json" \
  --data '{"title": "Full Stack Developer Nanodegree","description": "This goal of the Full Stack Web Developer Nanodegree program is to equip learners with the unique skills they need to build database-backed APIs and web applications."}'
```

```
curl --request GET \
  --url https://udacity-student-hub.herokuapp.com/api/v1/nanodegrees
```
