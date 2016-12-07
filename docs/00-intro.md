# what is a docker

### Traditional Virtualization

* [Paravirtualization](https://en.wikipedia.org/wiki/Paravirtualization) KVM, Xen, VMWare, Virtualbox
  * extremely secure, great for hosts.

[AWS EC2](https://aws.amazon.com/) |
[Mesos](http://mesos.apache.org)

### LXC / Cgroups

VMs without the hypervisor. cgroups (google @2005). Jailed execution environment (Solaris Zones / FreeBDS Jails). Ability to limit resource
usage.

Concepts:
  * lightweight -- no hypervisor overhead
    * supports _many_ more "VMs" per machine
  * Template driven. Mounted root filesystem.

[Proxmox](https://www.proxmox.com/en/) | [Mesos](http://mesos.apache.org)

### Docker

Concepts:
  * Run a single process in the foreground, no "guest OS" overhead.
    * 1 nginx container, 1 redis container, 1 phpfrpm container
    *  docker provides many conveniences for grouping and networking ([docker-compose](https://github.com/docker/compose)), sharing data ([volumes](https://docs.docker.com/engine/tutorials/dockervolumes/)), logging, and resource limiting.
  * Containers are immutable. Like old school EC2 w/o EBS.
  * Fast booting -- useful for utilities, e.g. containerized git! [dex](https://github.com/dockerland/dex)
  * Layered filesystem

[Docker Cloud](https://www.docker.com/products/docker-cloud) |[Mesos](http://mesos.apache.org)

##### Dockerfile

* Dockerfile
  * docker image
  * registry
    * tag demo
