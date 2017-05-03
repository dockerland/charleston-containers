# creating a local swarm

Lets use [docker-machine]() and the [docker-machine-kvm](https://github.com/dhiltgen/docker-machine-kvm) driver to create a local docker swarm of KVM instances.

Local KVM instances are very fast and cost nothing!


> For **production use** we recommend using [hashicorp terraform](https://www.terraform.io) for provisioning a swarm in cloud infrastructure. There is a [very cool tutorial]([See here](https://solinea.com/blog/multi-cloud-docker-swarm-terraform-ansible) on bootstrapping a cross-cloud [AWS + GCE] swarm cluster using [terraform]((https://www.terraform.io) and [ansible](https://ansible.org).


### dependencies

* Linux
  * On MacOS? run in a linux virtual machine or use the Virtualbox (or VMWare) [driver](https://docs.docker.com/machine/drivers/) instead.
  * On Windows? run in a linux virtual machine or use the Hyper-V [driver](https://docs.docker.com/machine/drivers/) instead.


* KVM, qemu, libvirt, dnsmasq
  ```sh
  # debian/ubuntu
  apt-get install libvirt-bin qemu-kvm dnsmasq

  # archlinux
  pacman -S qemu dnsmasq
  ```
  * unless you're root, your user must be added to the libvirt group as well
    ```sh
    sudo usermod -aG libvirt,kvm $(id -un)
    ```
  * be sure virtualization is not disabled by your BIOS; `lsmod | grep kvm` should show `kvm_intel` or `kvm_amd` -- https://wiki.archlinux.org/index.php/KVM#Loading_kernel_modules


* 'default' libvirtd network
  * the kvm driver does not create the 'default' network. it's easiest to do so via `virt-manager` > edit > connection details > virtual networks > default -- and **enable it on boot**.


* [docker-machine-kvm](https://github.com/dhiltgen/docker-machine-kvm) driver
  * download from [releases](https://github.com/dhiltgen/docker-machine-kvm/releases) if available, or
  * build from source (requires Go -- prefer 1.8.1+ and `libvirt`/`libvirt-dev`)
  ```sh
  export GOPATH="${GOPATH:-$HOME/go}"
  mkdir -p $GOPATH/src/github.com/dhiltgen/docker-machine-kvm
  cd $GOPATH/src/github.com/dhiltgen/docker-machine-kvm
  git clone git@github.com:dhiltgen/docker-machine-kvm.git .
  go get -v -d ./...
  go install -v ./cmd/docker-machine-driver-kvm
  [[ "$PATH" == *"$GOPATH/bin"* ]] || sudo cp -a $GOPATH/bin/docker-machine-driver-kvm /usr/local/bin/
  ```


### create swarm

Lets use a custom `MACHINE_STORAGE_PATH` when interacting with our swarm. This way we won't clutter up what we already have.
* `docker-machine` stores machine configurations under `~/.docker/machine` **by default** (e.g. if MACHINE_STORAGE_PATH is not set.)
* whenever using `docker-machine` to interact with our local swarm, remember to set `MACHINE_STORAGE_PATH=~/.docker-swarms/local`. shell scripts help...

> The machine documentation provides information on [Specifying Docker Swarm options for the created machine](https://docs.docker.com/machine/reference/create/#specifying-docker-swarm-options-for-the-created-machine). These options refer to "**classic swarm**", and not the "swarm mode" introduced in docker 1.12. We'll disregard these and manually run `init` and `join` commands on the machines themselves.


##### create swarm master

```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# create the master
docker-machine create -d kvm local-swarm-manager &&\
docker-machine ssh local-swarm-manager \
  docker swarm init --advertise-addr $(docker-machine ip local-swarm-manager)
```

##### create swarm worker nodes
```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# fetch the join token from manager
join_token="$(docker-machine ssh local-swarm-manager \
  docker swarm join-token worker -q )"
join_ip="$(docker-machine ip local-swarm-manager)"

# create worker nodes a, b, and c
for name in local-swarm-worker-{a..c}; do
  docker-machine create -d kvm $name &&\
  docker-machine ssh $name \
    docker swarm join --token "$join_token" "$join_ip" &&\
  echo -e "\e[1m$name\e[21m joined the swarm"
done
```

##### poll swarm info

lets make sure our swarm is running with 3 worker nodes and a manager.

```sh
export MACHINE_STORAGE_PATH=~/.docker-swarms/local

# activate the local swarm manager for this session...
eval $(docker-machine env local-swarm-manager)
docker node ls
```

For more on swarm, see https://docs.docker.com/engine/swarm/

Lets continue with configuring secrets in this swarm...
