# Set up wg-node on your server

> Follow these simple steps to set up **wg-node** on your own server!

## Step 1. Ensure that your kernel supports WireGuard

!!! quote "From [official WireGuard documentation](https://www.wireguard.com/compilation#kernel-requirements)"

    **WireGuard** requires Linux ≥3.10, with the following configuration options, which are likely already configured in your
    kernel, especially if you're installing via distribution packages.

    * `CONFIG_NET` for basic networking support
    * `CONFIG_INET` for basic IP support
    * `CONFIG_NET_UDP_TUNNEL` for sending and receiving UDP packets
    * `CONFIG_CRYPTO_ALGAPI` for crypto_xor

## Step 2. Install docker and docker compose plugin

**wg-node** is being run in docker containers, so the only dependencies you need to install are
[docker](https://www.docker.com/) and [docker compose plugin](https://docs.docker.com/compose/).

You can find installation instructions by clicking on these links:

* [installation instructions for **docker**](https://docs.docker.com/engine/install/)
* [installation instructions for **docker compose plugin**](https://docs.docker.com/compose/install/)

## Step 3. Set up `WIREGUARD_PUBLIC_HOSTNAME` environmental variable in the `.env` file

`WIREGUARD_PUBLIC_HOSTNAME` environmental variable should be set to your machine's public IP or
domain name, which is associated with the machine, for example `example.com` or `1.2.3.4`.

The variable should be located in the `./.env` file.
You can use `./.env.example` file as template to avoid typos:

```shell
cp ./.env.example ./.env
```

```dotenv title=".env"
# public hostname of the server
WIREGUARD_PUBLIC_HOSTNAME=<SERVER-IP-ADDRESS-OR-DOMAIN-NAME>

```

## Step 4. Set up docker secrets

!!! note

    It would be useful to read about docker secrets from the
    [docker documentation](https://docs.docker.com/engine/swarm/secrets/),
    if you have never heard about them.

### Step 4.1. Create directory for docker secrets

At first create `./secrets` directory and some subdirectories inside it, where all docker secrets will be located:

```shell
mkdir secrets
mkdir secrets/node
mkdir secrets/mongo
```

### Step 4.2 Set up secrets for the MongoDB container (`wg-node-mongo`)

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