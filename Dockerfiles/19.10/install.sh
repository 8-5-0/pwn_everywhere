#/bin/sh -e
export http_proxy="http://docker.for.mac.host.internal:1087"
export HTTP_PROXY="http://docker.for.mac.host.internal:1087"
export https_proxy="http://docker.for.mac.host.internal:1087"
export HTTPS_PROXY="http://docker.for.mac.host.internal:1087"
echo "[*]installing pwntools"
pip2 install  pwntools
pip2 install  ipython
pip2 install  ropper
echo "[*]installing gef"
wget -O /root/.gdbinit-gef.py -q https://github.com/hugsy/gef/raw/master/gef.py 
echo source /root/.gdbinit-gef.py >> ~/.gdbinit
echo "[*]installing oh-my-zsh"
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
mv /.zshrc -f /root/.zshrc
echo "[*]installing zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
echo "[*]installing one_gadget"
gem install one_gadget
gem install seccomp-tools