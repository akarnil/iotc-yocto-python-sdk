####	*For a Quick Start initiation into IoTConnect, we recommend the [MaaxBoard-IoTC-Voyager-Demo](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-yocto-c-sdk/voyager-demo/MaaxBoard-IoTC-Voyager-Demo.md). This pre-configured Yocto image facilitates a rapid onboarding of the MaaXBoard with IoTConnect, ensuring immediate data visibility in the cloud.
## MaaxBoard Example
In this MaaXBoard Example, developers are guided on how to integrate the `meta-iotconnect` and `meta-myExampleIotconnectLayer` meta-layers into a Yocto build image. The aim is to expedite Linux development, allowing developers to focus on their unique applications rather than the intricacies of cloud connection.

* Notes:
	* Based on the MaaXBoard [Development Guide](https://www.avnet.com/wps/wcm/connect/onesite/35645cc9-4317-4ca0-a2fa-30cce5f9ff17/MaaXBoard-Mini-Linux-Yocto-Lite-Development_Guide-V1.0-EN.pdf?MOD=AJPERES) from [this page](https://www.avnet.com/wps/portal/us/products/avnet-boards/avnet-board-families/maaxboard/maaxboard?utm_source=hackster)
	* Tested on Ubuntu 20.04 without issue.

The final directory structure is shown below:
   ```bash
   $ tree -L 2 imx-yocto-bsp/
   imx-yocto-bsp/
   ├── maaxboard
   │   └── build
   └── sources
      ├── base
      ├── meta-browser
      ├── meta-clang
      ├── meta-freescale
      ├── meta-freescale-3rdparty
      ├── meta-freescale-distro
      ├── meta-imx
      ├── meta-iotconnect
      ├── meta-maaxboard
      ├── meta-myExampleIotconnectLayer
      ├── meta-nxp-demo-experience
      ├── meta-openembedded
      ├── meta-python2
      ├── meta-qt5
      ├── meta-timesys
      └── poky
   ```

1. Install required packages
   ```bash
   sudo apt update && \
   sudo apt install -y gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential
   chrpath socat libsdl1.2-dev xterm sed cvs subversion coreutils texi2html docbook-utils
   python-pysqlite2 help2man make gcc g++ desktop-file-utils libgl1-mesa-dev libglu1-mesa-dev
   mercurial autoconf automake groff curl lzop asciidoc u-boot-tools cpio sudo locales python
   ```
1. Install repo
   ```bash
   curl https://storage.googleapis.com/git-repo-downloads/repo > ./repo && \
   chmod a+x repo && \
   sudo mv repo /usr/bin/
   ```
1. Download meta layers from NXP using repo
   ```bash
   mkdir -p imx-yocto-bsp && \
   cd imx-yocto-bsp && \
   repo init -u https://github.com/nxp-imx/imx-manifest  -b imx-linux-hardknott -m imx-5.10.35-2.0.0.xml && \
   repo sync
   ```

All instructions will take place from the `imx-yocto-bsp` directory unless stated otherwise.

1. Download Maaxboard sources
   ```bash
   git clone https://github.com/Avnet/meta-maaxboard.git -b hardknott sources/meta-maaxboard
   ```
1. Download this repo
   ```bash
   wget https://github.com/avnet-iotconnect/iotc-yocto-python-sdk/archive/refs/heads/hardknott.zip && \
   unzip hardknott.zip -d sources/ && \
   mv sources/iotc-yocto-python-sdk-hardknott/meta-* sources/ && \
   rm -r hardknott.zip sources/iotc-yocto-python-sdk-hardknott/
   ```
1. Configure the build (Note you will have to do this only for the first time setup, running the  command again will delete your local configuration)
   ```bash
   MACHINE=maaxboard source sources/meta-maaxboard/tools/maaxboard-setup.sh -b maaxboard/build
   ```
1. Initialise the Bitbake environment (Only if you need to do so again after completing the previous step)
   ```bash
   source sources/poky/oe-init-build-env maaxboard/build
   ``` 

1. Edit build configuration to include these layers
   ```bash
   echo -e '\nBBLAYERS += "${BSPDIR}/sources/meta-iotc-python-sdk"' >> conf/bblayers.conf && \
   echo -e '\nBBLAYERS += "${BSPDIR}/sources/meta-my-iotc-python-sdk-example"' >> conf/bblayers.conf
   ```

1. Add the IoTConnect Python SDK to `build/conf/local` image
   ```bash
   echo -e '\nIMAGE_INSTALL += " iotc-demo-dev packagegroup-core-boot kernel-modules"' >> conf/local.conf 
   ```
1. build!
   ```bash
   bitbake core-image-base
   ```
### Testing

Instructions for using a serial adapter and UART are found [here](https://www.hackster.io/monica/getting-started-with-maaxboard-headless-setup-24102b)  

If you haven't already added a user, you can add the default user `root` with password `avnet` to your `build/conf`

from the `imx-yocto-bsp` directory

   ```bash
   echo -e '\nEXTRA_IMAGE_FEATURES=""
   INHERIT += "extrausers"
   EXTRA_USERS_PARAMS = "\ 
   \tusermod -P avnet root; \ 
   "' >> conf/local.conf 
   ```

```bash
# Include systemd to your `local.conf`
echo -e '\nDISTRO_FEATURES_append = " systemd"\nDISTRO_FEATURES_BACKFILL_CONSIDERED += " sysvinit"\nVIRTUAL-RUNTIME_init_manager = " systemd"\nVIRTUAL-RUNTIME_initscripts = " systemd-compat-units"\n' >> /conf/local.conf
```

If you are using X509 certs make sure to add the certificates to your example layer before building in
`meta-my-iotc-python-sdk-example/recipes-apps/iotc-telemetry-and-commands-demo/files/certs`

Make sure to create your own `config.json` based off the examples in `meta-my-iotc-python-sdk-example/recipes-apps/iotc-telemetry-and-commands-demo/files/eg-private-repo-data` (place `config.json` in the same directory as the examples)

To run the test from `meta-my-iotc-python-sdk-example`, use the following command after connecting to the board
   ```bash
   /usr/bin/local/iotc/iotc-demo.py /usr/local/iotc/config.json
   ```
