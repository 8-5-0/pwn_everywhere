#/bin/sh -e
export http_proxy="http://docker.for.mac.host.internal:1087"
export HTTP_PROXY="http://docker.for.mac.host.internal:1087"
export https_proxy="http://docker.for.mac.host.internal:1087"
export HTTPS_PROXY="http://docker.for.mac.host.internal:1087"
pip3 install --upgrade pip
pip2 install --upgrade pip
echo "[*]installing pwntools"
pip3 install  pwntools
pip2 install  pwntools
pip3 install  ipython
pip3 install  ropper
echo "[*]installing gef"
git clone https://github.com/hugsy/gef /root/gef
echo "source /root/gef/gef.py" >> ~/.gdbinit
echo "[*]installing oh-my-zsh"
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
mv /.zshrc -f /root/.zshrc
echo "[*]installing zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
echo "[*]installing one_gadget"
gem install one_gadget
wget "https://raw.githubusercontent.com/kuangyujing/dracula-xfce4-terminal/master/Dracula.theme"
mkdir -p /root/.local/share/xfce4/terminal/colorschemes
mv Dracula.theme /root/.local/share/xfce4/terminal/colorschemes/Dracula.theme
unset http_proxy
unset HTTP_PROXY
unset https_proxy
unset HTTPS_PROXY