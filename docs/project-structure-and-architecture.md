# Project structure and architecture

> It is not necessary, but always useful to understand the project structure and architecture before using it!

So, let's dive in!

## Project architecture

The project architecture consists of two parts (and docker containers):

- **wg-node-app** - web server which listens for API requests and manages WireGuard config & connections.
- **wg-node-mongox** - MongoDB instance where information about clients' is stored.
  MongoDB's data directory will be mounted to `./.mongo-data` by default.

## Project directories and files (essentials)

### Docker secrets (`./.secrets` directory)

There are three _docker secrets_ in this project:

- `mongo_initdb_root_username` (file) - root user username for the MongoDB container.
- `mongo_initdb_root_password` (file) - root user password for the MongoDB container.
- `node_clients_public_keys` (directory) - contains files in PEM format with node clients' public keys,
  for example:

```
  -----BEGIN RSA PUBLIC KEY-----
  todo
  -----END RSA PUBLIC KEY-----

```

### File containing environmental variables which are necessary to be set (`./.env` file)

At the moment there is only one environmental variable which is necessary to be set up before running
**wg-node**. It is `WIREGUARD_PUBLIC_HOSTNAME` and it has to be specified inside `./.env` file.
The easiest way to create this file is to use the example file (`.env.example`):

```shell
cp ./.env.example ./.env
```

```dotenv
# public hostname of the server
WIREGUARD_PUBLIC_HOSTNAME=
```

Other useful environmental variables can be found inside `docker-compose.yaml`.
But it is more likely that you will never need to update them.

---

Okay! I think it is everything you need to know for now about the project structure and architecture.
Now you have an image of what it looks like. :)