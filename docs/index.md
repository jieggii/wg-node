# Welcome to wg-node documentation!

> Deploy and manage your Wireguard nodes with one hand!

**wg-node** is an application which provides you a simple way to run and manage Wireguard node.
Run in docker container and manage it effortlessly through HTTP REST API.

You can set up multiple Wireguard nodes on different servers and manage them all safely and easily
from a single machine.

**wg-node** is mostly inspired by [wg-easy](https://github.com/wg-easy/wg-easy), but is more minimalistic
and has some noticeable key differences:

- No UI, only HTTP REST API.
- All requests to the API must be signed using public RSA key, which is known by server running wg-node.
- Uses MongoDB to store clients instead of JSON files.

The application can be run on any GNU/Linux machine whose kernel supports WireGuard (linux 5.6+).
