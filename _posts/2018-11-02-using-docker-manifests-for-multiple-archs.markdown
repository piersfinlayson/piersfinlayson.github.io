---
layout: post
title:  "Using docker manifests to create multiple architecture containers"
date:   2018-11-02 16:31:00 +0000
categories: docker containers manifests
---

# Introduction

As part of creating a [multi-architecture ESP8266 build container](/esp8266/espressif/sdk/docker/containers/2018/11/02/esp8266-build-container.html) I had to get to grips with docker's experimental manifest commands.  It seems like they're fairly immature and not that well understood and documented at the moment.

The high-level process for building a multi-architecture container is to:

- Create a container for each architecture independently.

- Create a manifest - which looks like a container - but isn't and rather links to separate containers, for example one for each supported architecture.

There's an extra complexity if you want to use a single Dockerfile for the containers for both architectures, and if you need to build them from different base containers - as I have done with the ESP8266 SDK build container.  There I've used an Ubuntu base for x86-64 and Rasbian for ARM.  In order to share a Dockerfile you need a single common FROM command at the beginning of the Dockerfile, hence you need to create a manifest to create a multiple architecture FROM container, from which you then build the architecture specific containers.  See [here](https://github.com/piersfinlayson/otbiot-docker/tree/master/esp8266-build) for more details on that approach.

# Enabling Manifest Commands

Before you can use docker's manifest commands, because they are currently an experimental feature, you need to enable these on both the server and client.

On Ubuntu to enable experimental features on the server edit your docker config file:

```
sudo vi /etc/systemd/system/docker.service.d/docker.conf
```

To add the experimental argument:

```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -s overlay2 -H fd:// --experimental=true
```

Now restart the docker service:

```
sudo systemctl restart docker
```

Then enable experimental features on the client by editing the client config file:

```
vi /home/$USER/.docker/config.json
```

So it contains the following (just add the experimental bit to the existing config file within the curly braces):
```
{
        "experimental": "enabled"
}
```

If you now run docker version you should see that experimental features are enabled for both the client and server:

```
$ docker version
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        e68fc7a
 Built:             Tue Aug 21 17:24:56 2018
 OS/Arch:           linux/amd64
 Experimental:      true

Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       e68fc7a
  Built:            Tue Aug 21 17:23:21 2018
  OS/Arch:          linux/amd64
  Experimental:     true
```

I don't know precisely what version of docker you need for manifest support - but expect it's at least 18 onwards.

# Building a Manifest

Once you have enabled experimental features and have the containers built for each architecture, and have them uploaded to your repo server (such as hub.docker.com), first create the manifest like this:

```
docker manifest create my-repo/my-manifest:version my-repo/container-amd64:version my-repo/container-arm:version
```

Then annotate each container, with the correct architecture and OS, like so:

```
docker manifest annotate my-repo/my-manifest:version my-repo/container-amd64:version --arch amd64 --os linux
docker manifest annotate my-repo/my-manifest:version my-repo/container-arm:version --arch arm --os linux
```

Next check your manifest looks correct by inspecting it (the example here is pinched from ubuntu:18.04):

```
$ docker manifest inspect my-repo/my-manifest:version
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1150,
         "digest": "sha256:6b9eb699512656fc6ef936ddeb45ab25edcd17ab94901790989f89dbf782344a",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1150,
         "digest": "sha256:5b0b4ee0a78af051edb7f0ebd3a02ed08bc957162a978f641cd78ea3512d59dc",
         "platform": {
            "architecture": "arm",
            "os": "linux",
            "variant": "v7"
         }
      },
   ]
}

```

Finally, push the manifest to the repo server.  It is important you use the purge option, which clears the manifest locally once uploaded - otherwise you won't be able to create a new manifest in future, as there doesn't appear to be a docker manifest delete command.

```
docker manifest push --purge my-repo/my-manifest:version
```

# Running the Manifest as a Container

You can now run the combined manifest as if it were a container thus on any supported architecture:

```
docker run my-repo/my-manifest:version
```