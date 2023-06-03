# wg-node `<- WORK IN PROGRESS`


Deploy and manage your Wireguard nodes with one hand! 

**wg-node** (aka Wireguard node) provides you a simple way to run and manage Wireguard node.
Run in docker container and manage it effortlessly through HTTP REST API.

## Regards
The project is mostly inspired by [wg-easy/wg-easy](https://github.com/wg-easy/wg-easy) and copies it in some parts. 
But when creating **wg-node** I wanted to have something lighter and safer, something, that can be used
on multiple servers and with a lot of client peers and something that can be managed from a single machine. 
that's why there is HTTP REST API instead of cute UI and are request signatures.

## Dependencies
**Production:**
- Docker
- Docker compose plugin

**Development:**
* Python
* [PDM](https://github.com/pdm-project/pdm)

## How to run and use?
Please refer to the [project documentation]().