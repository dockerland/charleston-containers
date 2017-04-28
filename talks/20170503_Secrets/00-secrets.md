## secret best practices

* No secret should be written to disk in cleartext — ever
* No secret should be transmitted over a network in cleartext — ever
* All secret lifecycle and access events should be recorded in an incorruptible audit log
* Nonce secrets should be utilized if possible
* Secret versioning or rolling should be easier to accomplish than revealing cleartext


### standalone

* https://github.com/square/keywhiz
* https://github.com/hashicorp/vault

### infrastructure

* [swarm](swarm.md) - https://docs.docker.com/engine/swarm/secrets/
* https://docs.mesosphere.com/1.8/administration/secrets/
* https://docs.rancher.com/rancher/v1.4/en/cattle/secrets/



#### container

* [build vs. runtime](build-vs-runtime.md)
*
