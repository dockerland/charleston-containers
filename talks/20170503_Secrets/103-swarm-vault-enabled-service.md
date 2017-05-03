# adding a vault-enabled service to our local swarm

Lets add a service to the swarm that utilizes secrets from the `hashicorp-vault` service [we previously created](103-swarm-vault.md).

strangelove is a python application that serves http requests via [tornado](http://www.tornadoweb.org/) and uses the [hvac](https://github.com/ianunruh/hvac) client library to interact with hashicorp vault.

## build strangelove service image

Lets add an image to our [local swarm](100-swarm-mk.md) that will be used to start our vault-enabled service.

We'll use the [strangelove/Dockerfile](strangelove/Dockerfile) to build the base image for this service.

Because we're not using a registry, lets build the image on **all** swarm nodes. **this is extremely inefficient and unreliable -- use a registry**.

```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# build strangelove image
cd strangelove

for __node in $(docker-machine ls -q); do
  (
    eval $(docker-machine env $__node)
    docker build -t strangelove .
  )
done
```

## create the strangelove service

Our strangelove application listens on port 8888. Lets run it as a global
service (on **all** cluster nodes), hijacking port 9999 and mapping to port 8888
of our container. We do this to demo basic docker capabilities and principals.

```sh
# activate the local swarm manager for this session...
eval $(docker-machine env local-swarm-manager)

docker service create \
  --name strangelove \
  --mode global \
  --publish 9999:8888 \
  --network vault-network \
  strangelove

# poll until ready...
docker service ps strangelove
```

> **important!** From now on, we'll assume the local swarm manager is activated and no longer reference `eval $(docker-machine env local-swarm-manager)`

OK our strangelove service should be running. Lets visit it by making a http request to port 9999 of _any_ node.

```sh

# get random node
random_node="$(docker-machine ls -q | sed -n "$(( ( RANDOM % $(docker-machine ls -q | wc -l) )  + 1 ))p")"
random_node_ip=$(docker-machine ip $random_node)

curl $random_node_ip:9999
```

Auth code not loaded? Lets add it to our service!

## add vault secret to strangelove

strangelove first needs to authenticate with vault so it can read our secret launch code. Lets use our swarm secrets to inject the root token under `/run/secrets/vault-token`. This demonstrates adding secrets using `service update`. Keep in mind **updating a service causes it to restart**.


```sh
docker service update \
  --secret-add source=acme-vault-root-v1,target=vault-token \
  strangelove

# checkout the rolling update... lets use docker service ps
docker service ps strangelove
```

## confirm launch codes

By providing the vault token, the [strangelove application](strangelove/server.py) can extract the launch code we added [previously](102-swam-vault.md#add-secret-launch-codes-to-vault) to vault.

Lets see it work!

```sh

# get random node
random_node="$(docker-machine ls -q | sed -n "$(( ( RANDOM % $(docker-machine ls -q | wc -l) )  + 1 ))p")"
random_node_ip=$(docker-machine ip $random_node)

curl $random_node_ip:9999
```

Does it match?

![strangelove-launch-code](http://3.bp.blogspot.com/-JW4UrC1einc/UvhkaJEh3BI/AAAAAAAAFaY/ABJQJaMVHmE/s1600/919111_334149953354892_868150705_o.jpg)
