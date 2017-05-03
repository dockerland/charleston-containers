# adding secrets to our local swarm


## about swarm secrets

* Secrets are abvailable in **Docker 1.13 and higher**

* In terms of Docker Swarm services, a secret is a blob of data, such as a password, SSH private key, SSL certificate, or another piece of data that should not be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

* Swarm secrets are mounted into services under `/run/secrets` as a [readonly] tmpfs filesystem. They are never exposed as environment variables, nor can they be committed to an image if the docker commit command is run.

* A given secret is only accessible to those services which have been granted explicit access to it, and only while those service tasks are running. ecrets are encrypted during transit and at rest in a Docker swarm.

* See [official documentation](https://docs.docker.com/engine/swarm/secrets/) on swarm secrets for more information and an example of using secrets in a MySQL + Wordpress service.


#### adapting an application to use secrets

Because secrets are mounted under `/run/secrets`, applications must be adapted to access secrets through filesystem.
```js
token = process.env['ACME_TOKEN'];
```
becomes
```js
token = fs.readFileSync('/run/secrets/acme-token');
```


## example secret

Lets add a secret to our [local swarm](100-swarm-mk.md). Following our best practices, we'll version and namespace -- and mount the secret into services without the version. This makes rotation easier.

```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# activate the local swarm manager for this session...
eval $(docker-machine env local-swarm-manager)

echo "Abcracadabra" | docker secret create acme-password-v1 -
```

> **important!** From now on, we'll assume the local swarm manager is activated and no longer reference `eval $(docker-machine env local-swarm-manager)`

Lets see if our secret is registered;

```sh
docker secret ls
```

Notice the secret ID. That's not it's value ("Abracadabra"). We can use `docker secret inspect` to get the value. Secrets can be binary blobs of data (we created ours via stdin `-`)..


#### sharing our secret

Now lets add our secret to a service. You can do this during `service create`, or to a running service via `service update`. Keep in mind **updating a service causes it to restart**.

As a demo we're creating a service that hosts the contents of /run/secrets. **Don't do this at home!**.

```sh
docker service create \
  --name secret-spew \
  --publish 8080:80 \
  --replicas 1 \
  --secret source=acme-password-v1,target=acme-password \
  jrelva/nginx-autoindex \
    sh -c "cd /usr/share/nginx ; rm -rf html ; ln -s /run/secrets html && exec nginx -g 'daemon off;'"
```

###### Is our secret-spewer spewing secrets?

Lets check that our spewing secret service is running...

```sh
docker service ps secret-spew
```

Cool. Lets spew some secrets!
```
SWARM_IP=$(docker-machine ip local-swarm-manager)

# list secrets
curl $SWARM_IP:8080

# print our secret
curl $SWARM_IP:8080/acme-password
```

Whoa! Lets do something useful now. How about adding [hashicorp vault](https://www.vaultproject.io/) as to our swarm and using it to provide secrets to other containers in our swarm?
