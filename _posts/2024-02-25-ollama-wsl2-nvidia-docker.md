---
layout: post
title:  "Running ollama laptop with NVIDIA GPU, within WSL2, using docker"
date:   2024-02-25 7:01 +0000
tags:   ollama llm ai nvidia mx250 docker container
---

I've been playing around with LLMs on machines at home, starting with a Raspberry Pi 5 (super slow), all the way up to on a Windows gaming PC, with an NVIDIA 3060Ti.  However, as the laptop I use most of the time has an NVIDIA MX250 on-board I wanted to get ollama working with that, within WSL2, and within docker.

The steps I had to take were:
* Install the latest NVIDIA graphics driver for the MX250
* Install the NVIDIA CUDA tools
* Install NVIDIA container toolkit
* Reconfigure Docker Desktop
* Run ollama within a container

## Latest NVIDIA graphics driver

Within Windows Device Manager, my MX250 was showing up under Display adaptors.  I thought this was a good start, bu the driver installed was from 2019, and Windows insisted it was the latest version.  I went [here](https://www.nvidia.com/en-gb/geforce/drivers/) and downloaded and installed the latest for the MX200 series of devices.  In Device Manager I'm now showing:
* Driver Date: 15/02/2024
* Driver Version: 31.0.15.5161

I rebooted after this step (even though I wasn't prompted).

## Install NVIDIA CUDA tools

I then followed [Microsoft's "Enable NVIDIA CUDA on WSL](https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl) instructions, specifically following the steps on [NVIDIA's website](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network) following this path:
* Operating System: Linux
* Architecture: x86_64
* Distribution: WSL-Ubuntu
* Version: 2.0
* Installer Type: deb(network)

After this I had the tools installed within ```/usr/local/cuda``` and checked they were installed correctly as follows:

```
$ /usr/local/cuda/bin/nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Wed_Nov_22_10:17:15_PST_2023
Cuda compilation tools, release 12.3, V12.3.107
Build cuda_12.3.r12.3/compiler.33567101_0
```

## Install NVIDIA container toolkit

I installed the NVIDIA container toolkit using [these instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

While I did run this command to configure docker:

```
$ sudo nvidia-ctk runtime configure --runtime=docker
```

## Reconfigure Docker Desktop

I realised this wouldn't configure my docker instance (not least because nvidia-ctk told me daemon.json was empty), as I'm using Windows Docker Desktop.  So I pulled the config from ```/etc/docker/daemon.json``` and added to Docker Desktop -> Settings -> Docker Engine and hit "Apply & Restart":

```
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    }
```

I then checked NVIDIA support had been added to Docker:

```
$ docker info | grep -i nvidia
WARNING: No blkio throttle.read_bps_device support
WARNING: No blkio throttle.write_bps_device support
WARNING: No blkio throttle.read_iops_device support
WARNING: No blkio throttle.write_iops_device support
WARNING: daemon is not using the default seccomp profile
 Runtimes: io.containerd.runc.v2 nvidia runc
```

## Optional - Install ollama directly

If you don't want to run ollama within a container, at this point you can install it directly within WSL2 - and this should detect the NVIDIA GPU:

```
$ curl -fsSL https://ollama.com/install.sh | sh
>>> Downloading ollama...
######################################################################### 100.0%######################################################################### 100.0%
>>> Installing ollama to /usr/local/bin...
>>> Adding ollama user to render group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
>>> NVIDIA GPU installed.
```

## Run ollama within a container

However, I tend to run stuff as containers using docker.  First step here is to set up a local directory in order to mount in the container, so the downloaded models persist on the local filesystem:

```
$ mkdir ~/container-data/ollama/ollama
```

Then to run the container I created a script ~/container-data/ollama/start-cont.sh as follows:

```
#!/usr/bin/bash
docker rm -f ollama-gpu
docker run --restart always -d --name ollama-gpu --gpus=all -v ~/container-data/ollama/ollama:/root/.ollama ollama/ollama
```

Then to run:
```
chmod +x ~/container-data/ollama/start-cont.sh
~/container-data/ollama/start-cont.sh
```

## Checking GPU support

To check the container was using my NVIDIA GPU I tailed the container logs:

```
$ docker logs -f ollama-gpu
time=2024-02-25T11:17:03.130Z level=INFO source=images.go:710 msg="total blobs: 0"
time=2024-02-25T11:17:03.130Z level=INFO source=images.go:717 msg="total unused blobs removed: 0"
time=2024-02-25T11:17:03.131Z level=INFO source=routes.go:1019 msg="Listening on [::]:11434 (version 0.1.27)"
time=2024-02-25T11:17:03.131Z level=INFO source=payload_common.go:107 msg="Extracting dynamic libraries..."
time=2024-02-25T11:17:07.103Z level=INFO source=payload_common.go:146 msg="Dynamic LLM libraries [cuda_v11 rocm_v5 rocm_v6 cpu cpu_avx cpu_avx2]"
time=2024-02-25T11:17:07.103Z level=INFO source=gpu.go:94 msg="Detecting GPU type"
time=2024-02-25T11:17:07.103Z level=INFO source=gpu.go:265 msg="Searching for GPU management library libnvidia-ml.so"
time=2024-02-25T11:17:07.103Z level=INFO source=gpu.go:311 msg="Discovered GPU libraries: [/usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1 /usr/lib/wsl/drivers/nvhqig.inf_amd64_56b1629f0ce88717/libnvidia-ml.so.1]"
time=2024-02-25T11:17:07.368Z level=INFO source=gpu.go:99 msg="Nvidia GPU detected"
time=2024-02-25T11:17:07.368Z level=INFO source=cpu_common.go:11 msg="CPU has AVX2"
time=2024-02-25T11:17:07.375Z level=INFO source=gpu.go:146 msg="CUDA Compute Capability detected: 6.1"
```

Nice :-)

## Running a model

Obviously ollama isn't much use on its own - it needs a model.

To pull a model, such as llama2 (and this step is optional, as the subsequent run step will pull the model if necessary):

```
$ docker exec -ti ollama-gpu ollama pull llama2
docker exec -ti ollama-gpu ollama pull llama2
pulling manifest
pulling 8934d96d3f08... 100% ▕████████████████▏ 3.8 GB
pulling 8c17c2ebb0ea... 100% ▕████████████████▏ 7.0 KB
pulling 7c23fb36d801... 100% ▕████████████████▏ 4.8 KB
pulling 2e0493f67d0c... 100% ▕████████████████▏   59 B
pulling fa304d675061... 100% ▕████████████████▏   91 B
pulling 42ba7f8a01dd... 100% ▕████████████████▏  557 B
verifying sha256 digest
writing manifest
removing any unused layers
success
```

To run it:

```
$ docker exec -ti ollama-gpu ollama run llama2
>>> What are the advantages to WSL

 Windows Subsystem for Linux (WSL) offers several advantages over
traditional virtualization or emulation methods of running Linux on
Windows:

1. Performance: Running a full Linux kernel directly on Windows allows for
faster performance compared to emulation or virtualization, as the CPU and
memory are dedicated to the Linux environment without any abstraction
layers.
2. Ease of use: With WSL, you can easily switch between the Linux
environment and Windows, allowing you to take advantage of the strengths
of both operating systems.
...
```

## Results

These were disappointing.  I ended up getting around 2 tokens/s with this setup.

I could see around 10% NVIDIA GPU usage when responding, with around 1GB memory usage when the model was loaded.  I saw this ollama log which suggests the CPU is still doing the bulk of the work:

```
llm_load_tensors: offloaded 5/33 layers to GPU
```



what are the advantages of wsl

WSL laptop directly using GPU:
```
total duration:       5m6.946729681s
load duration:        9.605017ms
prompt eval count:    27 token(s)
prompt eval duration: 8.209514s
prompt eval rate:     3.29 tokens/s
eval count:           633 token(s)
eval duration:        4m58.721156s
eval rate:            2.12 tokens/s
```

WSL laptop container no GPU:
```
total duration:       3m24.818357217s
load duration:        3.140429ms
prompt eval count:    27 token(s)
prompt eval duration: 7.247851s
prompt eval rate:     3.73 tokens/s
eval count:           515 token(s)
eval duration:        3m17.565006s
eval rate:            2.61 tokens/s
```

WSL laptop container with GPU:
```
total duration:       5m13.205469553s
load duration:        387.997µs
prompt eval count:    27 token(s)
prompt eval duration: 7.805956s
prompt eval rate:     3.46 tokens/s
eval count:           670 token(s)
eval duration:        5m5.398036s
eval rate:            2.19 tokens/s
```

Windows laptop presumably with GPU, actually using WSL:
```
total duration:       4m51.888445617s
load duration:        3.273311ms
prompt eval count:    27 token(s)
prompt eval duration: 7.818108s
prompt eval rate:     3.45 tokens/s
eval count:           619 token(s)
eval duration:        4m44.053918s
eval rate:            2.18 tokens/s
```

Pi5 8GB (no GPU):
```
total duration:       5m17.896178043s
load duration:        435.042µs
prompt eval count:    27 token(s)
prompt eval duration: 10.736229s
prompt eval rate:     2.51 tokens/s
eval count:           649 token(s)
eval duration:        5m7.158631s
eval rate:            2.11 tokens/s
```

bigboy1 - windows
```
total duration:       6.352137s
load duration:        503.5µs
prompt eval count:    27 token(s)
prompt eval duration: 332.468ms
prompt eval rate:     81.21 tokens/s
eval count:           520 token(s)
eval duration:        6.017954s
eval rate:            86.41 tokens/s
```

bigboy1 - linux
```
total duration:       6.215398804s
load duration:        622.887µs
prompt eval count:    27 token(s)
prompt eval duration: 191.64ms
prompt eval rate:     140.89 tokens/s
eval count:           595 token(s)
eval duration:        6.022108s
eval rate:            98.80 tokens/s
```

bigboy1 - linux, no GPU:
```
total duration:       55.654405803s
load duration:        821.64µs
prompt eval count:    27 token(s)
prompt eval duration: 1.494639s
prompt eval rate:     18.06 tokens/s
eval count:           567 token(s)
eval duration:        54.157614s
eval rate:            10.47 tokens/s
```
This was fast enough to stay ahead of me reading, and subjectively seems about how fast internet LLMs perform.
