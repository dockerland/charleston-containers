# helpful docker concepts

### environmental variables

* programs cannot change the current environment, as they run in a [child process](https://en.wikipedia.org/wiki/Child_process)
  ```sh
  # ex A - demonstrate PID change in subshell
  $ echo "current pid: $BASHPID" ; ( echo "subshell pid: $BASHPID" )
  current pid: 15577
  subshell pid: 16614
  ```
  ```sh
  # ex B - like A, although manually created another instance of bash
  $ echo $$
  15577
  $ bash -c "eval echo \$$"
  16820
  ```
  
  > **takeaway** this is the reason we `eval` to set DOCKER_HOST using `docker-machine`
  ```sh
  eval $(docker-machine env machine-name)
  ```
  
* children inherit the parent environment. **environment variables MUST be exported**.
  ```sh
  $ NAME="goodnight moon"
  $ bash -c "echo hello $NAME"
  hello
  # use export or set -a to export vars...
  $ export NAME="goodnight moon"
  $ bash -c "echo hello $NAME"
  hello goodnight moon
  ```
  ```sh
  # list the last created container
  $ docker ps -n1 -q
  7b1180981b76
  # set DOCKER_HOST to something invalid (notice we do not export!)
  $ DOCKER_HOST="unknown_host"
  $ docker ps -n1 -q
  7b1180981b76
  # expected error above ^^^, lets pass invalid DOCKER_HOST var to child (same as export)
  $ DOCKER_HOST="unknown_host" docker ps -n1 -q
An error occurred trying to connect: Get http://unknown_host:2375/v1.24/containers/json?limit=3: dial tcp: lookup unknown_host: no such host
  # ^^^ yay, break all teh things.
  ```
  
  > **takeaway** assigning docker-machine persists to subshells/proccesses, but NOT to new shells.
  ```sh
  $ docker-machine env ocean-aaa
  export DOCKER_TLS_VERIFY="1"
  export DOCKER_HOST="tcp://104.255.255.255:2376"
  export DOCKER_CERT_PATH="/etc/blueacorn/docker-machine/machines/ocean-aaa"
  export DOCKER_MACHINE_NAME="ocean-aaa"
  ```
