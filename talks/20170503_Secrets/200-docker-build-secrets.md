# build-time secrets

At the time, there's nothing official for handling build time secrets in docker.


## leading candidate

I believe docker will introduce --mount to the Dockefile `RUN` command, which can be used to inject a secret (such as ssh private key) at build time.

* https://github.com/moby/moby/issues/32507

The trick is getting secrets (the ssh private key) into build context.

For now the easiest way to do this is via a build script that decrypts and copies a file in before running docker build, and then removes it after the build.

```
...
```


## workarounds

Despite not having an official approach, there's plenty of workarounds. A few things to keep in mind regarding the necessity of security;
  * will your image be published to a public repository?
  * is your engine available to the public?
  * never keep secrets around unencrypted, and NEVER, EVER check them in to a VCS unencrypted.

### build arguments

build arguments (`ARG` in Dockerfiles) must be avoided for secrets as they persist in the image (!) metadata.

```
$ docker build --build-arg SECRET=whisper ...
...
$ docker inspect -f '{{.ContainerConfig.Cmd}}' image-sha
```

* https://forums.docker.com/t/build-time-secrets/9684/6



##### buildtime "squash" example, risky.

* squash is an experimental feature in 1.13 and must be enabled
* squash is not intended to hide secrets

```
$ cat Dockerfile
...
COPY private.key /root/.ssh/id_rsa
RUN git pull git@github.com:acme/private-repo.git && rm -rf /root/.ssh/id_rsa
...

$ docker build --squash .
```


##### build scripts

* clone outside of Dockerfile, then `COPY` in contents.
```
...
```

* decrypt/copy a key into build context pre-build, and remove it post-build.

```
...
```


##### altfiles

* https://github.com/BenoitNorrin/docker-build-with-secrets


##### service hosting secrets + shell scipt


Lets do an example using netcat
```
...
```

Similar solutions;
* https://github.com/dockito/vault#how-it-works
* https://github.com/mdsol/docker-ssh-exec


Keep in mind;
  * docker-machine env -- keys missing from build context
  * service must be running

##### vault idea
https://groups.google.com/forum/#!msg/vault-tool/-nl973TywnI/SvJA6JBABQAJ
