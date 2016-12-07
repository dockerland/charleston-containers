# helpful docker hints

### follow the foreground process pattern

#### always log to stderr/stdout

```
logfile = /var/log/FAIL!

logfile = /dev/stdout
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
