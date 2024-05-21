## 安装wsl命令
``` bash
wsl --install
```
## 更改wsl默认版本
``` bash
sudo sed -i 's/http:/https:/g' /etc/apt/sources.list #中科大软件源
```

1. 卸载wsl
``` bash
wsl --unregister Ubuntu-20.04
```