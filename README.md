myvimconfig
===========
1.git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
2.copy the .vim directory to /root/.vim # if not using root,just copy it to ~/.vim
3.copy the vimrc file to /etc/vimrc
4.remeber to install the ctag package using “yum install ctags*"
5.ctags -R * to generate the tags file.
6.change the vimrc file for the tags path  "set tags=/autotest/tags" /autotest/tags is the directory of your tags file
7.create the file ~/.vimrc and add the only line "colorscheme molokai"

