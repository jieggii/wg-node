# wg-node

Deploy and manage your Wireguard nodes with one hand!

> Warning: work on the project is still in progress.

> **wg-node** (aka Wireguard node) provides you a simple way to run and manage Wireguard node.
> Run in docker container and manage it effortlessly through HTTP REST API.

## Regards

The project is mostly inspired by [wg-easy/wg-easy](https://github.com/wg-easy/wg-easy) and
is very similar to it in some parts.

However, when developing **wg-node** I wanted to create something lighter and safer;
something, that can be used on multiple servers and be managed from a single machine.
That's why there is HTTP REST API instead of cute UI and are request signatures.

## Dependencies

**Production:**

- Docker
- Docker compose plugin

**Development:**

* Python
* [PDM](https://github.com/pdm-project/pdm)

## How to run and use?

Please refer to the [project documentation](https://github.com/jieggii/wg-node).