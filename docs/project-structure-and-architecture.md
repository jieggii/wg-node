# Project structure and architecture

> It is not necessary, but always useful to understand the project structure and architecture before using it!

So, let's dive in!

## Docker containers

The project architecture consists of two parts (and docker containers):

- **wg-node** - web server which listens for API requests and manages WireGuard config & connections.
- **wg-node-mongo** - MongoDB instance where information about clients' is stored.
  MongoDB's data directory will be mounted to `./.mongo-data` by default.

## Project directories and files (essentials)

### Docker secrets (`./secrets` directory)

There are totally 4 docker secrets in this project:

- `mongo/username` - username for the MongoDB container.
- `mongo/password` - password for the MongoDB container.
- `mongo/database` - database name for the MongoDB container.
- `node/root_api_user_public_key` - root API user's public key.

### File containing environmental variables which are necessary to be set (`./.env` file)

At the moment, there is only one environmental variable which is necessary to be set up before running
**wg-node**. It is `WIREGUARD_PUBLIC_HOSTNAME` and it has to be specified inside `./.env` file.
The easiest way to create this file is to use the example file (`.env.example`):

```shell
cp ./.env.example ./.env
```

```dotenv title=".env"
# public hostname of the server
WIREGUARD_PUBLIC_HOSTNAME=
```

Other useful environmental variables can be found inside `docker-compose.yml`.
But it is more likely that you will never need to update them.

## API users

When you start **wg-node** for the first time, you already have only one API user—it is **root API user**.
It's public key is located in `./secrets/node/root_api_user_public_key`.
The only difference between root API user and other API users is that only root user
can create and delete API users.

---

Okay! I think it is everything you need to know for now about the project structure and architecture.
Now you have an image of what it looks like. :)