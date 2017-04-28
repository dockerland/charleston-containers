### runtime vs. buildtime

##### buildtime "squash" example, risky.
```
$ cat Dockerfile
...
COPY private.key /root/.ssh/id_rsa
RUN git pull git@github.com:acme/private-repo.git
...

$ docker build --squash .
```

* squash added in 1.13 as experimental, not intended to hide secrets.
* work is being done;
  * https://github.com/moby/moby/pull/30637
  * SECRETS directive https://github.com/moby/moby/pull/30637#issuecomment-279588146


##### altfile workaround
https://github.com/BenoitNorrin/docker-build-with-secrets

##### vault idea
https://groups.google.com/forum/#!msg/vault-tool/-nl973TywnI/SvJA6JBABQAJ

##### custom ssh config

```
Host *
    IdentityFile /run/secrets/id_rsa
```
