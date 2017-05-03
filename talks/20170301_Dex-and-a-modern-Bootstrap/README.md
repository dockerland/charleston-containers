# dex and a "modern" bootsrap

[dex](https://github.com/dockerland/dex) is a package manager for application containers. It is used to distribute and execute tooling (like `git`, `ffmpeg`, and `javac`) as well as daemons (like `redis`, `selenium`, and `caddy`).

We wrote dex to provide consistency and convenience around the _installation_ and _execution_ of application containers, and to  _improve tooling management_ in our developer bootstrap.


## a modern approach

installed dex applications are;
 * **portable** - they use docker to run the same way no matter the OS
 * **independent** - applications get their own HOME directory by default
 * **non-obtrusive** - will not clobber system installed software, DEX_BIN_DIR is set to ~/.dex/bin by default


many tools can be managed in a single command;
```sh
dex install --pull --force acme/
# ^^^ install all images from the "acme" repositry, pulling any changes first
```

Let's familiarize ourselves with the [dex quickstart](https://github.com/dockerland/dex#quickstart).

## lets build a bootstrap

** bootstrap** | _noun_ | boot·strap | \ˈbüt-ˌstrap\
* a loop at the back of a boot, used to pull it on so you can quickly start marching around in the mud.
* computing a technique of loading things into a computer by means of a few initial instructions.

Using [dex](https://github.com/dockerland/dex) as part of your developer onboarding process can save a lot of time. When internal tooling leverages `dex` provided variants, a developer can get rolling **in their first hour**, and patched tools can be made immediately available. Tooling based on dex provides;
* **consistent versions** - no need to ask developer "which ansible version?"
* **reduced maintenance** - a single repository where tools are versioned, tagged, distributed from

We also allow **allow developers to use their preferred OS/environment** with this approach. There's no need to fiddle with dependencies and versions or to install `java8`, `python2`, `make`, or `coreutils` on the first day!

### makeup of a dex bootstrap

#### the bootstrap script

A script needs to be created that interfaces with dex and installs tools and shell additions. This script should be;
  * **idempotent** - we want to run our bootstrap early and often. before submitting a bug, ask "did you run bootstrap?"
  * **fast running** - executing the bootstrap should be quick. if a dex image takes a long time to build from a Dockerfile, it should be published to a registry*
  * **accessible** - available to run without jumping through hoops. lets host it on an easy to remember domain.

The basic of the components of our bootstrap script will;
  * setup ~/.acme
  * install dex to ~/.acme/bin
  * install and update tooling (from our dex repositories) under ~/.acme/bin
  * add ~/.acme/shellrc to user's shell file (which adds ~/.acme/bin to user's PATH)

The full script is available in the [acme-bootstrap](https://github.com/dockerland/acme-bootstrap) repository [here](https://github.com/dockerland/acme-bootstrap/blob/master/acme-bootstrap)


#### the dex repo

We use a custom dex repository for tools the bootstrap installs. Multiple repositories can be used to satisfy different roles. The repository gives us a single place to maintain tooling which allows for an efficient and intuitive lifecycle.

Dex can use **any** git repository that has a dex-images/ folder as a valid endpoint, including local repositories.

As an example for the "acme" organization, we created https://github.com/dockerland/acme-bootstrap which holds the dex images (tooling) as well as the bootstrap script.


### going live with the bootstrap

Once you have a bootstrap script and dex repository in place, it's time to make it available to your users. In this case we'll make it available via http, so you can curl it. E.g.

```sh
$ curl http://acme-bootstrap.cc.dockerland.org/ | bash
```

Of course we publish and start the thing via a docker composition. See the [acme-bootstrap repository](https://github.com/dockerland/acme-bootstrap)

## other ideas for using dex

#### as an environment "wrapper"

See the [nodewrap](https://github.com/dockerland/acme-bootstrap/tree/master/dex-images/nodewrap) image from bootstrap as an example of wrapping commands in an environment pre-seeded with dependencies.

E.g.

```sh
$ node -v
bash: node: command not found
$ nodewrap node
v6.8.0
$ nodewrap yarn install
...
```

#### as a dependency manager

[idea](https://github.com/dockerland/dex/issues/51): a `dex.vars` in a project/repo root. run `eval $(dex up)`, which reads `dex.vars` and installs tools listed under `dex.vars` under `.dex/bin/` (relative to project/repo root), and adds `.dex/bin/` to PATH -- thanks @twslade
