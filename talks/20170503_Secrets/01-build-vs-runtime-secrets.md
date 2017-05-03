# build vs runtime secrets

Consider that containers are executed from prebuilt images.

When secrets are used to build an image -- such as a private key used to clone a git repository -- we call these 'build' secrets.

When secrets are injected into a running container -- such as providing an application API token -- we call these 'runtime' secrets.

Unfortunately no official mechanism exists for build-time secrets, although work is being done. We'll look at some strategies in [200-docker-build-secrets.md](200-docker-build-secrets.md)

## runtime secret patterns

### environmental variables

You may see reference to using environment variables for secrets, e.g.
`docker run -e MYSQL_ROOT_PASSWORD=whisper mysql` -- this is **deprecated!**.


### adapting a service to use secrets

* From Docker docs: The WordPress image has been updated so that the environment variables which contain important data for WordPress, such as WORDPRESS_DB_PASSWORD, also have variants which can read their values from a file (WORDPRESS_DB_PASSWORD_FILE). This strategy ensures that backward compatibility is preserved, while allowing your container to read the information from a Docker-managed secret instead of being passed directly.

### link to secrets in configuration

##### nginx example
```
$ cat /etc/nginx/site.conf
server {
    listen                443 ssl;
    server_name           localhost;
    ssl_certificate       /run/secrets/site.crt;
    ssl_certificate_key   /run/secrets/site.key;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
```

##### ssh-config example
```
$ cat ~/.ssh/config
Host *
    IdentityFile /run/secrets/id_rsa
```


##### docker swarm

As of docker 1.13, there's an official solution for runtime secrets.

Lets dive deep into docker swarm secrets, starting with  [creating a local swarm](100-swarm-mk.md).
