Dota2Analytics
==============================

## 🚨 Warning: This project is currently undergoing restructuring. 😎 

Please avoid using it at the moment and patiently await further updates.
--------

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
    - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
    - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
    - 🤖 An automatically generated frontend client.
    - 🦇 Dark mode support.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.

## How To Use It

You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

> [!IMPORTANT]
> ``docker-compose up -d --build``

## ML Development
1. First, yo need to create a virtual environment by running `make create_environment` on the root directory of this project please make sure you have `make` installed on your machine before running this command or you can create a virtual environment by running `python3 -m venv venv` and activate the virtual environment by running `source venv/bin/activate`
2. Then, you need to install the dependecies by running `make requirements` on the same directory where `requirements.txt` located
3. Create `.env` file at the root directory of this project/repo or copy the `.env.example` and rename it to `.env`
4. Dota Key is required to run this project. You can get the key by registering at [OpenDota](https://www.opendota.com/) and get the key from the profile page.

> [!IMPORTANT]  
> Crucial please add the make coomand when you create a new command. It will help you to understand the command that you want to run. For example, if you want to get data process you can run `make data`


### How to Use this Tool After Doing Setup?
all this project is create with Makefile. Thus, you can run the command by using `make` command. Here are the list of command that you can use:


1. `make data` : This command will run the scrapping process. It will get the data from OpenDota website and store the result to CSV

2. `make requirements` : This command will install all the dependencies that listed at `requirements.txt`

3. `make create_environment` : This command will create a virtual environment for this project

4. `make clean` : This command will remove the virtual environment and all the dependencies that installed on the virtual environment

> [!IMPORTANT]  
> Crucial please add the make coomand when you create a new command. It will help you to understand the command that you want to run. For example, if you want to get data process you can run `make data`


## Application Development

### Configure

`.env.example` -> `.env`

You can then update configs in the `.env` files to customize your configurations.

Before deploying it, make sure you change at least the values for:

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`
- `OPEN_DOTA_KEY`

You can (and should) pass these as environment variables from secrets.

Read the [deployment.md](./deployment.md) docs for more details.

### Generate Secret Keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

## Backend Development

Backend docs: [backend/README.md](./backend/README.md).

## Frontend Development

Frontend docs: [frontend/README.md](./frontend/README.md).

## Development

General development docs: [development.md](./development.md).

This includes using Docker Compose, custom local domains, `.env` configurations, etc.

## Release Notes

Check the file [release-notes.md](./release-notes.md).

## License

The Full Stack FastAPI Template is licensed under the terms of the MIT license.