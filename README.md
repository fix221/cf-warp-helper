# cf-warp-helper

简体中文 | [English](https://github.com/Fix221/cf-warp-helper/blob/main/README-EN.md)
一个一键选择cloudflare warp最优服务器的工具

## 功能

- 自动选择cloudflare warp最优服务器
- 自动更新cloudflare warp服务器列表
- 自动通过wireguard客户端连接cloudflare warp服务器
- 自动生成wireguard配置文件

## 使用方法

1. 下载并安装[wireguard](https://www.wireguard.com/install/)客户端（或从本仓库直接下载wireguard-installer.exe）
2. 克隆或下载本仓库[cf-warp-helper](https://github.com/fix221/cf-warp-helper/archive/refs/heads/main.zip)
3. 修改wg-sample.conf中的`[Interface]`部分的`PrivateKey`和`[Peer]`部分的`PublicKey`为cloudflare warp服务器提供的密钥
4. 打开cmd或powershell，进入cf-warp-helper目录，输入命令`python main.py`
5. Enjoy!

## 注意事项

- 本工具仅供学习交流使用，请勿用于商业用途。

## 鸣谢

- [cloudflare](https://www.cloudflare.com/)提供的免费warp服务
- [Misaka-blog](https://gitlab.com/Misaka-blog)大佬提供的cfwarp优选脚本
