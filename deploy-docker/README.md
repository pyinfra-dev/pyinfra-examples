This is an example how to install `docker` with `PyInfra`.

The example follows the `ansible` playbook [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker).

In this example I've tried to stay as much as possible close to the original, using the same variables and program logic. My original purpose was to also compare `ansible` and `PyInfra` using a well known real life example.

Use as follows:

```shell
pyinfra 10.1.2.3 deploy-docker/deploy.py --ssh-user root
```

And test if it was successfully  installed with:

```shell
ssh root@10.1.2.3 docker run hello-world
```
