## How to use it
- [Install docker](https://docs.docker.com/install/)
- [Install docker-compose](https://docs.docker.com/compose/install/) (be sure that docker-compose version is at least 1.9.0).
- only on MacOSX: ```brew install coreutils``` to install ```greadlink```
- Get searx-docker
```sh
cd /usr/local
git clone https://github.com/searx/searx-docker.git
cd searx-docker
```
- Generate MORTY_KEY ```sed -i "s|ReplaceWithARealKey\!|$(openssl rand -base64 33)|g" .env```
- Edit the other settings in [.env](https://github.com/searx/searx-docker/blob/master/.env) file according to your need
- Check everything is working: ```./start.sh```,
- ```cp searx-docker.service.template searx-docker.service```
- edit the content of ```WorkingDirectory``` (SEARX_DIR environment variable) in the ```searx-docker.service``` file (only if the installation path is different from /usr/local/searx-docker)
- Install the systemd unit :
```sh
systemctl enable $(pwd)/searx-docker.service
systemctl start searx-docker.service
```

## Note on the image proxy feature

The searx image proxy is activated by default using [Morty](https://github.com/asciimoo/morty).

The default [Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) allow the browser to access to {SEARX_HOSTNAME} and ```https://*.tile.openstreetmap.org;```.

If some users wants to disable the image proxy, you have to modify [./Caddyfile](https://github.com/searx/searx-docker/blob/master/Caddyfile). Replace the ```img-src 'self' data: https://*.tile.openstreetmap.org;``` by ```img-src * data:;```

## Custom docker-compose.yaml

Do not modify docker-compose.yaml otherwise you won't be able to update easily from the git repository.

It is possible to the [extend feature](https://docs.docker.com/compose/extends/) of docker-compose :
- stop the service : ```systemctl stop searx-docker.service```
- create a new docker-compose-extend.yaml, check with ```start.sh```
- update searx-docker.service (see SEARX_DOCKERCOMPOSEFILE)
- restart the servie  : ```systemctl restart searx-docker.service```
