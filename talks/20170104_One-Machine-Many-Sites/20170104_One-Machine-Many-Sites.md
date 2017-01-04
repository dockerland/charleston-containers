# One Machine, Many Sites

Or, how I learned to stop worrying and love not writing virtualhost definitions.

* _Jan 2017 [Charleston Containers](https://www.meetup.com/Charleston-Containers/) fail by Brice Burgess ([@IceburgBrice](https://twitter.com/IceburgBrice))_

### Overview

---------------

* Use [docker machine](https://github.com/docker/machine) to create a vultr cloud instance.
  > why vultr? we wanted to try! There's also some great promos to make it affordable for our group. Please use http://www.vultr.com/?ref=7078147-3B to create an account if you signup (you'll get $20, we'll get $30).

* Containerize a website and a HTTP file server

  > We'll need containerized applications to run on our machine. Lets try hosting the official [Docker Documentation](https://github.com/docker/docker.github.io) built with Jekyll and the HTTP/2 web server [CADDY](https://caddyserver.com/) for serving files.

* Pick a reverse proxy to allow our machine to host multiple containerized sites.

  > A single process can bind to a port at a time. Lets pick one to listen on :80 and :443 that will auto-discover our "web" containers and also give us {hassel,}**free SSL** through [letsencrypt](http://letsencrypt.org/)!

* Tie it all together

  > Lets start our proxy and sites on our machine, update some DNS records, and cross our fingers.

-----------------


# docker-machine me a machine

[docker machine](https://github.com/docker/machine) is a minimal CLI tool for managing and interacting with [docker engine](https://github.com/docker/docker) across a bunch of different providers. We're going to try using it with [vultr cloud](http://www.vultr.com/?ref=7078147-3B) today.
> machine is far from the only orchestrator. There's [Docker for AWS](https://www.docker.com/aws) which handles setting up an ELB-backed swarm cluster and related VPC rules. There's [Openshift](https://www.openshift.com/) which we hope to have demo'd to the group. And **many, many** more. We're going with machine because it's minimal and locally available.


#### installation

machine requires docker, and is often preinstalled (e.g. if you use [Docker for Mac](https://docs.docker.com/docker-for-mac/)). To install manually, we recommend grabbing 0.9+ via the [GitHub releases page](https://github.com/docker/machine/releases).

```sh
# Linux, 0.9.0-rc2 example.
$ curl -L https://github.com/docker/machine/releases/download/v0.9.0-rc2/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
    chmod +x /tmp/docker-machine &&
    sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
```

#### add vultr support to docker-machine

machine does not support vultr out of box. we'll need to add it via a plugin. feel free to use the virtualbox or generic driver if you want to experiment locally, or the AWS|DigitalOcean|Azure|OpenStack support if you're already setup elsewhere.

Follow instructions from https://github.com/janeczku/docker-machine-vultr


```sh
# Linux, v1.1.0 example.
curl -L https://github.com/janeczku/docker-machine-vultr/releases/download/v1.1.0/docker-machine-driver-vultr-v1.1.0-linux-amd64.tar.gz | tar xz && \
sudo mv docker-machine-driver-vultr /usr/local/bin
```

##### set free a vultr

time to see what [vultr cloud](http://www.vultr.com/?ref=7078147-3B) is all about. signup, enable the API under "Account", and get your [API Token](https://my.vultr.com/settings/#settingsapi).

> I like to store API tokens in a vault, or source them in files under my home directory. Here's an example:
  ```sh
  echo "VULTR_TOKEN=<YOUR_TOKEN>" > ~/.token-vultr && chmod 600 ~/.token-vultr
  ```

```sh
# create a machine named vultr-cc-1
. ~/.token-vultr
docker-machine create --driver vultr --vultr-api-key="$VULTR_TOKEN" vultr-cc-1
```

We now have a machine named `vultr-cc-1` !


# containerize a couple of sites

Lets host a mirror of the official [Docker Documentation](https://github.com/docker/docker.github.io). We can contain any web app, starting with writing a Dockerfile.

```sh
cd $(mktemp -d 2>/dev/null || mktemp -d -t 'darwin')
curl -L https://raw.githubusercontent.com/dockerland/charleston-containers/master/talks/20170104_One-Machine-Many-Sites/compositions/traefik/Dockerfile-docker-docs \
  > Dockerfile

docker build -t docker-docs .

# test it runs (on port 8080)
docker run --rm -p 8080:4000 docker-docs
```

To demonstrate multi-tenant support, lets also host a file server using the super awesome HTTP/2 web server [CADDY](https://caddyserver.com/).

```sh
echo "FROM abiosoft/caddy" > Dockerfile

docker build -t caddy-fs .
docker run --rm -p 8080:80 -v $(pwd):/srv caddy-fs
```


# pick a reverse proxy

This is a fun one.

Consider only one process can be bound to a port and the web is tied to ports 80 (http:// plaintext) and 443 (https:// TLS/SSL). We usually
have nginx or apache listening on these ports, and we usually use write virtualhost definitions for each site, and we usually spend time maintaining them.

Don't you think it would be great if we start a "web" container, and configuration is automatically made for it? No need to worry about virtualhost definitions?

We want to have multiple containerized sites/applications available on the web ports, so a reverse proxy is needed. Lets choose one that will;

  * listen to the docker socket and automatically create configuration for web containers
  * provide super helpful additions such as free SSL certificates and management.


At BlueAcorn we use [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) + [letsencrypt-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion).  [BlackGlory/caddy-proxy](https://github.com/BlackGlory/caddy-proxy) is a similar (docker-gen) based image that uses [caddy](https://caddyserver.com/). Examples for each are provided in [compositions/](compositions/)


For this demo, lets try to use [traefik](https://traefik.io/). It gives us what we need PLUS a pretty control panel. It also has an official image on docker hub.


```
docker run --rm \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  -v /dev/null:/traefik.toml \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  traefik --web --docker --docker.domain=docker.localhost --logLevel=DEBUG


# traefik reads container labels for configuration hinting
docker run -d \
  --label=traefik.frontend.rule=Host:whoami.docker.localhost \
  emilevauge/whoami

# test proxy to whoami container
curl -H Host:whoami.docker.localhost http://localhost/

# shiny backend
browser http://localhost:8080/
```

Full documentation on the traefik docker backend available [here](https://docs.traefik.io/toml/#docker-backend)


# laying down a fine oriental rug

To tie the machine together, lets;

* start services on our vultr cloud server.
* point DNS records to vultr cloud
* script a `docker-machine scp` helper to make file sharing easier.
* add SSL and HTTP basic auth to our file server
* protect the traefik dashboard
