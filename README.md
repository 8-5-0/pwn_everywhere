# Pwn with Docker in Mac OS

**Pwning under Mac!**

### Quick start

#### XQuartz
* download from https://www.xquartz.org/
* open it with command `open -a XQuartz`
#### Docker
* build image with Dockerfile
  *You can custimize Dockerfile, .zshrc and install.sh as you like.*
  
#### Key Components
```
zsh, pwntools, ipython, gef, oh-my-zsh, zsh-autosuggestions, one_gadget, vim, lxterminal
```

### 使用方法

```
python3 manage_pwn.py [-h] {run,attach,end} [--ubuntu] [version] [directory] [--priv]...

e.g. python3 manage_pwn.py run --ubuntu 18.04 ./ --priv
```

致谢：

* 项目思路来自于swing师傅：https://bestwing.me/Docker-for-Mac-and-run-gdb-GUI-window.html。
* manage_pwn 修改自 ancypwn https://github.com/WinMin/ancypwn/