# Run wg-node on your server

> When everything is set up properly, it's time to finally run WireGuard node.

Simply run the following command to build the necessary docker containers:

```shell
docker compose build
```

And another one to bring them up:

```shell
docker compose up
```

That's it! By default, web server is listening for port **80** and WireGuard is on port **51820**. 