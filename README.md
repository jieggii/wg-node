# wg-node

Deploy and manage your WireGuard nodes with one hand!

> Warning: work on the project is still in progress.

**wg-node** is an application which provides you a simple way to run and manage WireGuard node.
Run in docker container and manage it effortlessly through HTTP REST API.

You can set up multiple WireGuard nodes on different servers and manage them all safely and easily
from a single machine.

**wg-node** is mostly inspired by [wg-easy](https://github.com/wg-easy/wg-easy), but is more minimalistic
and has some noticeable key differences:

- No frontend UI, only HTTP REST API.
- All requests to the API must be RSA-signed using client's private key,
  whose public key is known by server running wg-node.
- Uses MongoDB instead of JSON files to store clients.

The application can be run on any GNU/Linux machine whose kernel supports WireGuard (linux 5.6+).

## Dependencies

**Production:**

- Docker
- Docker compose plugin

**Development:**

* Python
* [PDM](https://github.com/pdm-project/pdm)

## How to run and use?

Please refer to the [project documentation](https://jieggii.github.io/wg-node) (currently not up-to-date).
