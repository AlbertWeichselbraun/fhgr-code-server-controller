# FHGR Code Server Controller

1. Open the editor in a private window (this is necessary, since code stores settings in cookies which might become invalid, if files are no longer available)
2. We restart instances and delete all data once a day.

## Upgrade

Upgrade the code server to the latest version using
```bash
podman pull ghcr.io/albertweichselbraun/docker-code-server:latest
``` 

## Maintenance 

Plugin updates:
1. edit `template/hosts` to allow plugin updates
2. update the plugins in a code instance
3. copy them to `template/config.template`


## Security

To improve system security we recommend
1. restarting the containers once a day
2. regenerating the nginx mappings once a day

