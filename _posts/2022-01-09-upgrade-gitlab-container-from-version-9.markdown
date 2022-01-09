---
layout: post
title:  "Upgrading a gitlab-ce container from version 9"
date:   2022-01-09 7:00 +0000
tags:   gitlab github container docker
---

I installed a privately hosted of gitlab back in 2017, using what was presumably latest at the time - version 9.0.5-ce.0.  I decided to upgrade it today.  It's not a trivial exercise - so I've documented here.

Essentially you need to upgrade in stages, removing your old gitlab-ce container and then moving up to the last version in that major series, followed by the first in the next, and so on.  In my case I was on 9.0.5 so this meant I had to go through these versions:

* 9.0.5-ce.0 # Started with this
* 9.5.10-ce.0
* 10.0.0-ce.0
* 10.8.7-ce.0
* 11.0.0-ce.0
* 11.11.8-ce.0
* 12.0.0-ce.0
* 12.10.14-ce.0
* 13.0.0-ce.0
* 13.12.15-ce.0
* 14.0.0-ce.0
* 14.6.1-ce.0 # Latest as of writing

## First - Create a backup

Before anything else, take a backup of your current instance.  To do this on version 9, assuming your container is called gitlab, run the following:

```
docker exec -t gitlab gitlab-rake gitlab:backup:create
```

This will create a file in your gitlab data/backups directory called something like this:

```
1641713400_2022_01_09_gitlab_backup.tar
```

Also, backup your config/gitlab-secrets.json somewhere.

If you need to restore start up a new gitlab container of the version you started with (in my case 9.0.5-ce.0), put the files you backed up in the location where the gitlab container will look for them, and then run:

```
docker exec -ti gitlab gitlab-rake gitlab:backup:restore BACKUP=1641713400_2022_01_09_gitlab_backup.tar
```

You'll probably get asked if it's OK to overwrite the existing (blank) database - choose yes if you're happy this is the right thing to do!

## Get the images

Not necessary to do this as a separate step, but speeds up the subsequent upgrade process:

```
docker pull gitlab/gitlab-ce:9.0.5-ce.0
docker pull gitlab/gitlab-ce:9.5.10-ce.0
docker pull gitlab/gitlab-ce:10.0.0-ce.0
docker pull gitlab/gitlab-ce:10.8.7-ce.0
docker pull gitlab/gitlab-ce:11.0.0-ce.0
docker pull gitlab/gitlab-ce:11.11.8-ce.0
docker pull gitlab/gitlab-ce:12.0.0-ce.0
docker pull gitlab/gitlab-ce:12.10.14-ce.0
docker pull gitlab/gitlab-ce:13.0.0-ce.0
docker pull gitlab/gitlab-ce:13.12.15-ce.0
docker pull gitlab/gitlab-ce:14.0.0-ce.0
docker pull gitlab/gitlab-ce:14.0.12-ce.0 # version I decided to go with
```

## Now do the upgrade

To upgrade to a new version there are 4 steps:

* Stop the current container and waiting for it to shutdown
* Delete it
* Start a container with the next version in the process
* Monitor the logs, checking it succeeds
* Run some manual checks to ensure you can log in and your repos are still there

I wrote the following script to automate the first 4 steps above.  It takes the version to upgrade to as the only CLI arg. You will need to change the variables as appropriate for your instance.

```
#!/bin/bash
set -e

VERSION=$1
if [ -z $VERSION ]
then
        echo "Usage $0 <version>"
        exit
fi
HOSTNAME=gitlab.internal.packom.net
SSH_PORT=2222
HTTPS_PORT=8444
HTTP_PORT=8081
GITLAB_SHELL_SSH_PORT=2289
CONTAINER_NAME=gitlab
CONFIG_DIR=~/container-data/gitlab/config
LOG_DIR=~/container-data/gitlab/logs
DATA_DIR=~/container-data/gitlab/data

echo Updating gitlab to $VERSION
echo "- First stop old container"
docker stop gitlab
echo "- Now remove old container"
docker rm gitlab
echo "- Now start new container"
docker run -d --hostname $HOSTNAME --env GITLAB_OMNIBUS_CONFIG="external_url 'http://$HOSTNAME/'; gitlab_rails['gitlab_shell_ssh_port'] = $GITLAB_SHELL_SSH_PORT; gitlab_rails['backup_keep_time'] = 604800;" -p $HTTPS_PORT:443 -p $HTTP_PORT:80 -p $SSH_PORT:22 --name $CONTAINER_NAME --restart always -v $CONFIG_DIR:/etc/gitlab -v $LOG_DIR:/var/log/gitlab -v $DATA_DIR:/var/opt/gitlab gitlab/gitlab-ce:$VERSION
echo "- Tail new container's logs - Ctrl-C once update complete"
docker logs -f $CONTAINER_NAME
```

Save this script off (e.g. to update_one_version.sh) and then go through upgrading a step at a time as follows:

```
./update_one_version.sh 9.5.10-ce.0
```

One the container images are downloaded the process takes an hour or so - probably depends on the size of your database (repos).

I had one glitch, upgrading to 12.10.14-ce.0, hitting this error:

```
RuntimeError
    ------------
    Execution of the command `/opt/gitlab/embedded/bin/redis-cli -s /var/opt/gitlab/redis/redis.socket INFO` failed with a non-zero exit code (1)
    stdout:
    stderr: Could not connect to Redis at /var/opt/gitlab/redis/redis.socket: No such file or directory
```

However, the container restarted (as it was configured to do) and then came up successfully.

## Finishing up

You may want to prune your docker install once you've finished - getting rid of unnecessary images:

```
docker system prune
docker image prune -a
```
