# what is a docker

## Traditional Virtualization

* [Paravirtualization](https://en.wikipedia.org/wiki/Paravirtualization) KVM, Xen, VMWare, Virtualbox
  * extremely secure, _great for hosts_.

[AWS EC2](https://aws.amazon.com/) |
[Mesos](http://mesos.apache.org)

## LXC / Cgroups

VMs without the hypervisor. cgroups (google @2005). Jailed execution environment (Solaris Zones / FreeBDS Jails). Ability to limit resource
usage.

#####  more like a chroot (FTP home directory) than a VM

* lightweight -- no hypervisor overhead

##### template driven

* mounted root filesystem

##### scale-out

[Proxmox](https://www.proxmox.com/en/) | [Mesos](http://mesos.apache.org)

## Docker

The **future**.

##### Execute a single process, in the **foreground**. No "guest" OS overhead.
* Like the LXC template, but limits packaging to _application dependencies_.
* consistent runtime; completely portable.

    ```sh
    lxc-start -Fn debian-jessie
    root@debian-test:~# ps -auxw | head -n5
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root         1  0.0  0.1  28124  4220 ?        Ss   22:23   0:00 /sbin/init
    root        16  0.0  0.0  32968  3188 ?        Ss   22:23   0:00 /lib/systemd/systemd-journald
    root        65  0.0  0.1  55184  5476 ?        Ss   22:23   0:00 /usr/sbin/sshd -D
    root        69  0.0  0.0  12664  1772 tty1     Ss+  22:23   0:00 /sbin/agetty --noclear tty1 linux
    ```
    ```sh
    $ docker run -it --rm debian:jessie sh -c "ls ; ps -auxw"
    bin   dev  home  lib64	mnt  proc  run	 srv  tmp  var
    boot  etc  lib	 media	opt  root  sbin  sys  usr
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root         1  0.0  0.0   4336   748 ?        Ss+  22:26   0:00 sh -c ls ; ps -auxw
    root         8  0.0  0.0  17500  2080 ?        R+   22:26   0:00 ps -auxw
    ```

    > **takeaway** this is where the "land of PID:1" comes from, w/ exception of tiny-init being added to docker 1.13
    * 1 nginx container, 1 redis container, 1 phpfrpm container


##### Completely Transparent
* Dockerfiles are easy to read, and we get transparent ancestry.
    ```sh
    curl https://bitnami.com/redirect/to/137792/bitnami-redis-3.2.6-0-linux-ubuntu-14.04-x86_64.ova?bypassauth=false&fb=1&with_popup_skip_signin=1 > redis-3.2.6.ova
    vim redis-3.2.6.ova

    curl https://github.com/docker-library/redis/blob/2e14b84ea86939438834a453090966a9bd4367fb/3.2/Dockerfile > Dockerfile-redis-3.2.6
    vim Dockerfile-redis-3.2.6

    printf "FROM redis:3.2.6\n#my customizations" > Dockerfile
    ```

##### docker provides many conveniences for grouping and networking ([docker-compose](https://github.com/docker/compose)), sharing data ([volumes](https://docs.docker.com/engine/tutorials/dockervolumes/)), logging, and resource limiting.


##### Containers are immutable.
  * consistent runtime -- completely portable
  * Like old school EC2 w/o EBS.

##### Fast booting -- useful for utilities, e.g. containerized git!

  ```sh
  $ mkdir -p test/{a,b,c}
  $ time docker run -v $(pwd)/test:/work --workdir=/work ubuntu ls
  a
  b
  c

  real	0m0.656s
  user	0m0.023s
  sys	0m0.017s
  ```

  [dex](https://github.com/dockerland/dex)
  * contain your tooling deps! git, npm, even gitk!


##### Layered filesystem, know the build-cache

[Docker Cloud](https://www.docker.com/products/docker-cloud) |[Mesos](http://mesos.apache.org)

### Dockerfile

* Docker builds images from Dockerfiles.
* Containers are started from images.
* Images are published to registry. Registries may be self hosted using the "Registry Image"
  ```sh
  FROM registry:2

  COPY config.yml /etc/docker/registry/config.yml
  ```

  ```sh
  docker run -p 6379:6379 redis:2.8
  # ^^^ fetches from https://hub.docker.com/_/redis/

  docker run -p 6379:6379 secret-registry.com/redis:2.8
  # fetches from a private registry (self hosted)
  ```
    * Docker provides "OFFICIAL" repositories https://hub.docker.com/explore/

* Images may be arbitrarily tagged
  ```sh
  docker build -t test
  docker tag test secret-registry.com/redis:2.8
  docker run secret-registry.com/redis:2.8
  # ^^^ runs local
  docker pull secret-registry.com/redis:2.8 && docker run secret-registry.com/redis:2.8
  # ^^^ pulls from registry
  ```
