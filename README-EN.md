# cf-warp-helper
[简体中文](https://github.com/Fix221/cf-warp-helper/blob/main/README.md) | English

A tool for selecting the best cloudflare warp server and connecting to it using wireguard.

## Features

- Auto select the best cloudflare warp server
- Auto update cloudflare warp server list
- Auto connect to cloudflare warp server using wireguard client
- Auto generate wireguard config file

## Usage

1. Install and download [wireguard](https://www.wireguard.com/install/) client (or download wireguard-installer.exe from this repository)
2. Clone or download this repository [cf-warp-helper](https://github.com/cf-warp-helper/cf-warp-helper/releases)
3. Modify the `PrivateKey` and `PublicKey` in `wg-sample.conf` to the keys provided by cloudflare warp server
4. Open cmd or powershell, navigate to cf-warp-helper directory and run `python main.py`
5. Enjoy!

## Note

- This tool is for learning and communication only, and should not be used for commercial purposes.

## Acknowledgements 

- [cloudflare](https://www.cloudflare.com/) provides free warp service
- [Misaka-blog](https://gitlab.com/Misaka-blog) provides a script for selecting the best cfwarp server