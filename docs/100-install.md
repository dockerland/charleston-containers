# Installing Docker

## MacOS 

Docker has two options for installing on Mac. If your using an older version of OSX, you should use [Docker Toolbox](https://docs.docker.com/engine/installation/mac/#docker-toolbox). If your using a newer version of MacOS, you should use the newer 'Docker for Mac' which has better support.

### Requirements 

* Mac must be a 2010 or newer model, with Intel’s hardware support for memory management unit (MMU) virtualization; i.e., Extended Page Tables (EPT) macOS 10.10.3 Yosemite or newer
* At least 4GB of RAM
* VirtualBox prior to version 4.3.30 must NOT be installed (it is incompatible with Docker for Mac). Docker for Mac will error out on install in this case. Uninstall the older version of VirtualBox and re-try the install.


### installation

Check out the (installation guide)[https://docs.docker.com/docker-for-mac/] for more details. Basically, you will download the dmg image from the docker site, run the installer app bundled in the dmg, then run the app that gets installed to /Applications. This will add an item to your system tray. Once you complete the installation, you can check to see what versions by doing the following:

```sh 
$ docker --version
Docker version 1.13.0-rc3, build 4d92237

$ docker-compose --version
docker-compose version 1.9.0, build 2585387

$ docker-machine --version
docker-machine version 0.9.0-rc2, build 7b19591
```
