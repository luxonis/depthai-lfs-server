# DepthAI LFS Server

This tool serves files stored in [Giftless LFS Server](https://github.com/datopian/giftless) over HTTP via direct link (just like raw.githubusercontent.com)

## Setup

```
$ docker build -t depthai-lfs-server .
$ docker run -v <path_to_lfs_files>:/storage -e STORAGE_PATH=/storage -p <custom_port>:8080 depthai-lfs-server
```