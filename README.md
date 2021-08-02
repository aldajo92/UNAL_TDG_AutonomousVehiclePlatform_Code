## Configuring Docker ##

Before check if docker is installed:

```
docker run hello-world
```

```
sudo sh install-deps.sh
```

## Configure Docker Default Runtime

To enable access to the CUDA compiler (nvcc) during `docker build` operations, add `"default-runtime": "nvidia"` to your `/etc/docker/daemon.json` configuration file before attempting to build the containers:

``` json
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },

    "default-runtime": "nvidia"
}
```

You will then want to restart the Docker service or reboot your system before proceeding.

```
docker pull nvcr.io/nvidia/l4t-tensorflow:r32.5.0-tf2.3-py3
docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-tensorflow:r32.5.0-tf2.3-py3
```

<!-- sudo apt-get install -y arduino arduino-mk i2c-tools minicom -->

## I2C ##
i2cdetect -r -y N where N is the I2C bus number.

## References ##

- I2C detect: https://forum.legato.io/t/i2cdetect-shows-no-devices-on-the-bus/3502