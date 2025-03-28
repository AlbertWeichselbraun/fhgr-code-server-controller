export DATA_DIR=/home/albert/tmp/prog/config
export DOCKER_GROUP=$(getent group docker | cut -d: -f3)
mkdir -p ${DATA_DIR}
docker run --rm -it \
	--name=fhgr-code-server-{{port}} \
	--net=host \
	-e DISPLAY=:0 \
	-e TZ=Europe/Zurich \
	-e SUDO_PASSWORD=702e2f3b-d611-408c-ae95-64055eadafcd \
	-e DEFAULT_WORKSPACE=/config/workspace \
	-p 8443:8443 \
	-v ${DATA_DIR}:/config \
	--group-add $DOCKER_GROUP \
	fhgr-code-server


