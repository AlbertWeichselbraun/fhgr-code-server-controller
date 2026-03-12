#!/bin/bash

EXAM_DIRECTORY=/srv/fhgr-code-server-controller/vm/config.95*
DATE=$(date +"%y-%m-%d")

tar -cvzf exam-backup-$DATE.tar.gz $EXAM_DIRECTORY/workspace
