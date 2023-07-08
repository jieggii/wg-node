# Set up wg-node on your server

> To set up **wg-node** on your own server, you will need to follow some simple steps.

## Step 1. Ensure that your machine supports WireGuard

Please ensure that your kernel supports WireGuard. (#TODO: how?)

## Step 2. Install dependencies

**wg-node** is being run in docker containers, so the only dependencies you need to install are
[docker](https://www.docker.com/) and [docker compose plugin](https://docs.docker.com/compose/).

Install them and make sure that they are set up properly.

## Step 3. Set up `WIREGUARD_PUBLIC_HOSTNAME` environmental variable

`WIREGUARD_PUBLIC_HOSTNAME` environmental variable should be set to your machine's public IP or
domain name, which is associated with the machine, for example `example.com` or `8.8.8.8`.

The variable should be located in the `./.env` file.
You can use `./.env.example` file as template to avoid typos:

```shell
cp ./.env.example ./.env
```

```dotenv title=".env"
# public hostname of the server
WIREGUARD_PUBLIC_HOSTNAME=<SERVER-IP-ADDRESS-OR-DOMAIN-NAME>

```

## Step 4. Set up _docker secrets_

!!! note

    If you have never heard about docker secrets, it would be useful to read about them
    from the [docker documentation](https://docs.docker.com/engine/swarm/secrets/).

### Step 4.1. Create directory for docker secrets

At first create `./secrets` directory, where all docker secrets will be located:

```shell
mkdir -p "./secrets/mongo ./secrets/node"
```

### Step 4.2 Set up secrets for the mongodb container (wg-node-mongo)

`mongo/username`, `mongo/password` and `mongo/username` secrets stand for MongoDB user credentials and database name.
You need to come up with them yourself!

Then write them to the files:

```shell

echo "<USERNAME>" >> "./secrets/mongo/username"
echo "<PASSWORD>" >> "./secrets/mongo/password"
echo "<DATABASE-NAME>" >> "./secrets/mongo/database"
```

### Step 4.3 Set up `node/root_api_user_public_key` secret

`node/root_api_user_public_key` docker secret is a file, which contains public key of
the root API user (an API user is any single teapot or computer which has its
own public and private keys and whose public key is known by **wg-node** instance.

From the note above, we can see that we have to generate keypair somehow, and
write public key to `./secrets/node/root_api_user_public_key`.

Okay... Let's try!

To be continued...