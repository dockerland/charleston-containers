# helpful docker hints

### follow the foreground process pattern

#### always log to stderr/stdout

```
logfile = /var/log/FAIL!

logfile = /dev/stdout
```

#### handling multi-tenant port mapping

ideally one "app" per docker engine node. helpful tools;
* [nginx-proxy](https://github.com/jwilder/nginx-proxy)
* docker swarm
* manual binds
```sh
# print currently bound ports
$ lsof -i -n  | grep LISTEN
syncthing 3045 nesta   10u  IPv6  39024      0t0  TCP *:snapenetio (LISTEN)
syncthing 3045 nesta   16u  IPv4  38161      0t0  TCP 127.0.0.1:http-alt (LISTEN

# map port 8888 on local host to port 80 [nginx listen port] of container
$ docker run -it --rm -p 8888:80 nginx:1.11
```

### understand docker build cache


### bind mounts are not volumes

* avoid bind mounts in compositions unless you always intend to run that composition locally (and not on a swarm or machine). otherwise bootstrapping of the machines/nodes needs to happen.

### try musl but don't kill yourself over it

* docker hires Nataneal Copa from [alpine linux](https://alpinelinux.org/) in Feb 2016
* official images migrating to `:alpine` variant

```
$ for dist in alpine:latest ubuntu:latest node:latest node:alpine; do docker pull $dist ; done
$ docker images --filter=dangling=false --format "table {{.Size}}\t{{.Repository}}\t{{.Tag}}" | head -n5
SIZE                REPOSITORY          TAG
4.799 MB            alpine              latest
128.2 MB            ubuntu              latest
655.5 MB            node                latest
55.3 MB             node                alpine
```

* don't kill yourself over it.
  * glibc _works_ -- musl often _unsupported_ (though docker is changing this).
  * node-gyp fail for many module
  * use dex to test versions
  ```sh
  $ cd /my/node-project
  $ rm -rf node_modules
  $ dex run npm:alpine install
  npm info it worked if it ends with ok
  ...
  ```
  ```
  # dex run is npm:alpine install is @ equivalent of
  $ docker run -it --rm -v $(pwd):/work node:alpine sh -c 'cd /work ; npm install'
  npm info it worked if it ends with ok
  ...
  ```



### user and group mappings

monitoring must be container aware.
