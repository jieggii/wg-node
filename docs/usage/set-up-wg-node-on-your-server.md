# Set up wg-node on your server

> To set up **wg-node** on your own server, you will need to follow some simple steps.

## Step 1. Ensure that your machine supports WireGuard

Please ensure that your kernel supports WireGuard. (#TODO: how?)

## Step 2. Install dependencies

**wg-node** is being run in docker containers, so, the only dependencies you need to install are
[docker](https://www.docker.com/) and [docker compose plugin](https://docs.docker.com/compose/).

Install them and make sure that they are set up properly. (#TODO: more details)

## Step 3. Set up `WIREGUARD_PUBLIC_HOST` environmental variable

> `WIREGUARD_PUBLIC_HOST` environmental variable should be set to your machine's public IP or
> domain name, which is associated with the machine. (e.g. `example.com` or `8.8.8.8`).

The variable should be located in the `./.env` file.
Use `./.env.example` file as template to avoid typos:

```shell
cp ./.env.example ./.env
```

```dotenv
# public hostname of the server
WIREGUARD_PUBLIC_HOSTNAME=<SERVER_IP_ADDRESS_OR_DOMAIN_NAME>

```

## Step 4. Set up _docker secrets_

> [What are docker secrets?](https://docs.docker.com/engine/swarm/secrets/)

### Step 4.1. Create directory for docker secrets

At first create `./.secrets` directory, where all docker secrets will be located:

```shell
mkdir -p "./.secrets"
```

### Step 4.2 Set up `mongo_initdb_root_username` and `mongodb_initdb_root_password` secrets

`mongo_initdb_root_username` and `mongodb_initdb_root_password` secrets stand for MongoDB root user credentials.
You need to come up with them yourself!

Then write them to the files:

```shell
echo "<USERNAME>" >> "./.secrets/mongo_initdb_root_username"
echo "<PASSWORD>" >> "./secrets/mongo_initdb_root_password"
```

### Step 4.3 Set up `node_clients_public_keys` secret

> `node_clients_public_keys` docker secret is a directory, which contains files containing
> public keys (in PEM format) of known node clients
> (a node client is any single teapot or computer which has its own public and private keys and
> whose public key is listed in `node_clients_public_keys` secret on the server side).

From the note above, we can see that we have to generate keypair somehow, and
create file containing generated public key inside the
`./.secrets/node_clients_public_keys` directory.

Okay... Let's try!

To be continued...