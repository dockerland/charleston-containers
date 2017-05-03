## secret best practices

* No secret should be written to disk in cleartext — ever
* No secret should be transmitted over a network in cleartext — ever
* All secret lifecycle and access events should be recorded in an incorruptible audit log
* utilize nonce secrets if possible (e.g. secret engine creates one-time use keys for authenticating to a server - see [vault-ssh-helper](https://github.com/hashicorp/vault-ssh-helper))

* application to access secrets through filesystem;
  ```js
  token = process.env['SECRET_TOKEN'];
  ```
becomes
  ```js
  token = fs.readFileSync('/secrets/token');
  ```
* version and namespace secrets for easier rotations and a maintainable lifecycle; `acme-SECRET-v1` gets mounted as `.../acme-SECRET`



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
