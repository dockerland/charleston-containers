# adding hashicorp vault to our local swarm

Lets add [hashicorp vault](https://www.vaultproject.io/) to our swarm and use
it to share secrets to other services.

Vault is an enterprise secret service that sets best practices. Some reasons
for using it is the powerful audit long, and one-time/nonce passwords.

> **important!** We're going to use a _development_ mode version of vault for this demo. Typically
you'll want to use a production setup backed by consul, postgres, or files in a
distributed volume. There's a [nice tutorial](http://cloudacademy.com/blog/hashicorp-vault-how-to-secure-secrets-inside-microservices/) on doing just this.

## create the vault network

Lets add a network to our [local swarm](100-swarm-mk.md) that will be used by other services to interact with vault.

```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# activate the local swarm manager for this session...
eval $(docker-machine env local-swarm-manager)

# create network
docker network create --driver overlay vault-network
```

> **important!** From now on, we'll assume the local swarm manager is activated and no longer reference `eval $(docker-machine env local-swarm-manager)`


## create the vault service

We're going to create the vault service and expose its port (8200) to services on the swarm.

This is a development mode vault, so it will loose its secrets on restarts. We can go the distance and setup production in another talk...

```sh
docker service create \
  --name hashicorp-vault \
  --publish 8200 \
  --network vault-network \
  --replicas 1 \
  -e SKIP_SETCAP=1 \
  -e VAULT_ADDR=http://127.0.0.1:8200 \
  vault:0.7.0

# poll until ready...
docker service ps hashicorp-vault
```

* we skip memory locking (IPC_LOCK) as swarm does not yet support capabilities
* we set VAULT_ADDR to http:// vs https:// (default) -- we'll later exec into this container and use the `vault` command

## init vault, register secrets

The vault is deep and [RTFM](https://www.vaultproject.io/docs/index.html) applies. It must first be initialized before use. Initializing sets the cryptography using [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing), and we'll register it's keys in the Swarm for re-use and unsealing.

> **note** execing into swarm containers is trivial, as they're distributed and have replicas. I wrote a shell helper function to do the dirty work. You pass it the service name and command to run.

```sh
swarm/service/exec(){
  local service="$1" ; shift
  local replica=1
  local service_id="$(docker service ps -q $service --no-trunc)"
  local node="$(docker service ps --format "{{.Node}}" $service)"
  (
    eval $(docker-machine env $node)
    docker exec -it $service.$replica.$service_id $@
  )
}
# exec into vault service container
swarm/service/exec "hashicorp-vault" vault init
```

###### What? The vault is already initialized?

Because the official vault image runs vault in dev mode `vault server -dev`, it starts initialized and unsealed. We would typically see output like:

```sh
Unseal Key 2: 1pxViFucRZDJ+kpXAeefepdmLwU6QpsFZwseOIPqaPAC
Unseal Key 3: bw+yIvxrXR5k8VoLqS5NGW4bjuZym2usm/PvCAaMh8UD
Unseal Key 4: o40xl6lcQo8+DgTQ0QJxkw0BgS5n6XHNtWOgBbt7LKYE
Unseal Key 5: Gh7WPQ6rWgGTBRSMecuj8PR8IM0vMIFkSZtRNT4dw5MF
Initial Root Token: 5b781ff4-eee8-d6a1-ea42-88428a7e8815

Vault initialized with 5 keys and a key threshold of 3...
```

and would add the keys + root token to our swarm as secrets using `docker secret create`. Instead, lets examine the logs to figure the root token + keys...


```sh
swarm/service/logs(){
  local service="$1" ; shift
  local replica=1
  local service_id="$(docker service ps -q $service --no-trunc)"
  local node="$(docker service ps --format "{{.Node}}" $service)"
  (
    eval $(docker-machine env $node)
    docker logs $@ $service.$replica.$service_id
  )
}

# full output, the below grepping is fragile and can break if vault changes messaging.
swarm/service/logs "hashicorp-vault"

swarm/service/logs "hashicorp-vault" 2>/dev/null | grep "Unseal Key:" | awk '{print $NF}' | \
  docker secret create acme-vault-unseal-v1 -

swarm/service/logs "hashicorp-vault" 2>/dev/null | grep "Root Token:" | awk '{print $NF}' | \
  docker secret create acme-vault-root-v1 -
```

## add secret launch codes to vault

![strangelove-launch-code](http://3.bp.blogspot.com/-JW4UrC1einc/UvhkaJEh3BI/AAAAAAAAFaY/ABJQJaMVHmE/s1600/919111_334149953354892_868150705_o.jpg)

> Use the Root Token from logs in the previous step. We will set the pictured code as codes/strangelove in vault


```sh
# exec into vault service container
swarm/service/exec "hashicorp-vault" sh

# login using root token
vault auth <ROOT_TOKEN_FROM_LOGS>

# add the launch code the vault
vault write secret/strangelove value=FGD135
```

OK cool. We have vault running on the local swarm and added a secret launch code to it. Now lets start a service that interfaces with vault...
