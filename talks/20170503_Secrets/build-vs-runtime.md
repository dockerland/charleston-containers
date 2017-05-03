### runtime vs. buildtime


`ARG` - : build-time args persist in the image (!) as metadata, just not as environment variables at runtime.
```
$ docker inspect -f '{{.ContainerConfig.Cmd}}' image-sha
```

* https://forums.docker.com/t/build-time-secrets/9684/6


##### build script

clone outside of Dockerfile, then `COPY` in contents. Less transparency.

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
  * RUN --mount https://github.com/moby/moby/issues/32507


##### altfile workaround
https://github.com/BenoitNorrin/docker-build-with-secrets

##### vault idea
https://groups.google.com/forum/#!msg/vault-tool/-nl973TywnI/SvJA6JBABQAJ

##### PR



##### local service hosting secrets + shell scipt

https://github.com/dockito/vault#how-it-works
https://github.com/mdsol/docker-ssh-exec


flaws;

  * docker-machine env -- keys missing from build context
  * service must be running



##### custom ssh config

```
Host *
    IdentityFile /run/secrets/id_rsa
```
