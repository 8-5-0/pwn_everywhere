#/bin/sh -e
echo "[*]installing pwntools"
pip2 install  pwntools
pip2 install  ipython
echo "[*]installing gef"
wget -O /root/.gdbinit-gef.py -q https://github.com/hugsy/gef/raw/master/gef.py
echo source /root/.gdbinit-gef.py >> ~/.gdbinit
echo "[*]installing oh-my-zsh"
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
mv /.zshrc -f /root/.zshrc
echo "[*]installing zsh-autosuggestions"
git clone git://github.com/zsh-users/zsh-autosuggestions /root/.zsh/plugins/zsh-autosuggestions
echo "[*]installing one_gadget"
gem install one_gadget