# Introduction

> It is not necessary, but always useful to understand the project structure and architecture before using it!
> That's why this section is written.

So, let's dive in!

The project architecture consists of two parts (and docker containers):

* **wg-node-app** - web server which listens for API requests and manages WireGuard config & connections.
* **wg-node-mongo** - MongoDB instance where information about clients' is stored.