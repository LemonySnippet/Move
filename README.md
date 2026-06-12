# SETUP
1) install uv (I used it during development)
`curl -LsSf https://astral.sh/uv/install.sh | sh`

step 2: clone this repo
`git clone (...)`

Step 2.5: prepare the .env file in app/core/.env
`.env.boilerplate` guides you in the fields required to compile the file
NOTE: place the file **exactly** in app/core/.env

step 3: launch the app with the following command
`uv run uvicorn main:app --reload`

the app runs locally, therefore

step 4: open a browser and visit the swagger at
`localhost:8000/docs`

You can now test the endpoints.

step 5: if you want to run the tests, please use the following
`sudo apt install python3-pytest`
`cd Move`
`PYTHONPATH=. uv run pytest`

# DESIGN CHOICES
python: comfortable enough for efficient backend systems + lots of libraries already available with prod-grade code

fastAPI: standard choice for efficient APIs, native swagger, native async support (even though for this mock was not strictly needed, in production it smay become a good feature.

SQLite: quick prototyping, assignment specified that the build had not to be production-ready so other possible choices (such as PostGRESQL would have been overkill)

JWT: Stateless approach, quick to sketch and ideal for services that will become micro-services

data_models_db: (see db folder) quick db sketch for the prototype
data_models_api: (see schemas folder) quick sketch for the prototype + minimal management of credentials to avoid the publication of pwds as API responses 

user can access the secret-resource only with a valid bearer-token. The token lives for a maximum of 10 minutes. A token can be invalidated through the logout, in that case the token will not grant access to the resource anymore.


Pytest: Standard testing suite
