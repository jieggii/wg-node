# Welcome to wg-node documentation!

Deploy and manage your WireGuard nodes with one hand!

!!! warning

    Work on **wg-node** and its documentation is still in progress.
    Please feel free to contribute in any way to this project.

**wg-node** is an application which provides you a simple way to run and manage WireGuard node.
Run in docker container and manage it effortlessly through HTTP REST API.

You can set up multiple WireGuard nodes on different servers and manage them all safely and easily
from a single machine.

**wg-node** is mostly inspired by [wg-easy](https://github.com/wg-easy/wg-easy), but is more minimalistic
and has some noticeable key differences:

- No frontend UI, only HTTP REST API.
- All requests to the API must be RSA-signed using API client's private key,
  whose public key is known by server running **wg-node**.
- **MongoDB** is used to store information about peers.

The application can be run on any GNU/Linux machine whose kernel supports WireGuard (linux 3.10+).
