### runtime vs. buildtime

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


##### altfile workaround
https://github.com/BenoitNorrin/docker-build-with-secrets

##### vault idea

##### custom ssh config

```
Host *
    IdentityFile /run/secrets/id_rsa
```


### secret example
* The secrets are each mounted in a tmpfs filesystem at /run/secrets/mysql_password and /run/secrets/mysql_root_password. They are never exposed as environment variables, nor can they be committed to an image if the docker commit command is run. The mysql_password secret is the one used by the non-privileged WordPress container to connect to MySQL.
```
$ docker service create \
     --name mysql \
     --replicas 1 \
     --network mysql_private \
     --mount type=volume,source=mydata,destination=/var/lib/mysql \
     --secret source=mysql_root_password,target=mysql_root_password \
     --secret source=mysql_password,target=mysql_password \
     -e MYSQL_ROOT_PASSWORD_FILE="/run/secrets/mysql_root_password" \
     -e MYSQL_PASSWORD_FILE="/run/secrets/mysql_password" \
     -e MYSQL_USER="wordpress" \
     -e MYSQL_DATABASE="wordpress" \
     mysql:latest
```

```
$ docker service create \
    --name wordpress \
    --replicas 1 \
    --network mysql_private \
    --publish 30000:80 \
    --mount type=volume,source=wpdata,destination=/var/www/html \
    --secret source=mysql_password,target=wp_db_password,mode=0400 \
    -e WORDPRESS_DB_USER="wordpress" \
    -e WORDPRESS_DB_PASSWORD_FILE="/run/secrets/wp_db_password" \
    -e WORDPRESS_DB_HOST="mysql:3306" \
    -e WORDPRESS_DB_NAME="wordpress" \
    wordpress:latest
```

### secret rotation

```
$ docker service update \
     --secret-rm mysql_password mysql

$ docker service update \
     --secret-add source=mysql_password,target=old_mysql_password \
     --secret-add source=mysql_password_v2,target=mysql_password \
     mysql
```

* updating a service caused it to restart, thus MySQL has access to secret.

```
$ docker exec $(docker ps --filter name=mysql -q) \
    bash -c 'mysqladmin --user=wordpress --password="$(< /run/secrets/old_mysql_password)" password "$(< /run/secrets/mysql_password)"'
```

### as a compose (3.1) service

* https://docs.docker.com/compose/compose-file/#secrets

```yml
version: '3.1'

services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```

### cleanup

```
$ docker service rm wordpress mysql

$ docker volume rm mydata wpdata

$ docker secret rm mysql_password_v2 mysql_root_password
```


### symbolic links to secrets, even at runtime
```
$ cat site.conf
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
$ docker secret create site.conf site.conf

$ docker service create \
     --name nginx \
     --secret site.key \
     --secret site.crt \
     --secret site.conf \
     --publish 3000:443 \
     nginx:latest \
     sh -c "ln -s /run/secrets/site.conf /etc/nginx/conf.d/site.conf && exec nginx -g 'daemon off;'"
```


### adapting a service to use secrets

* When you start a WordPress container, you provide it with the parameters it needs by setting them as environment variables. The WordPress image has been updated so that the environment variables which contain important data for WordPress, such as WORDPRESS_DB_PASSWORD, also have variants which can read their values from a file (WORDPRESS_DB_PASSWORD_FILE). This strategy ensures that backward compatibility is preserved, while allowing your container to read the information from a Docker-managed secret instead of being passed directly.
