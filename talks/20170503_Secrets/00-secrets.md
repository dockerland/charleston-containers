# secrets

![whisper](http://3.bp.blogspot.com/_Pqpmm2T6j4g/Se157ygAT2I/AAAAAAAAHmA/BBWkN0IFZoM/s400/Secret.jpg)

When leaked, there's oogle eyes.


## overview

### best practices

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


### secret tools

#### standalone

* https://github.com/square/keywhiz
* https://github.com/hashicorp/vault
* https://github.com/codahale/sneaker

#### infrastructure

* [swarm](swarm.md) - https://docs.docker.com/engine/swarm/secrets/
* https://docs.mesosphere.com/1.8/administration/secrets/
* https://kubernetes.io/docs/concepts/configuration/secret/
* https://docs.rancher.com/rancher/v1.4/en/cattle/secrets/


Lets look at the difference between build and runtime secrets.
