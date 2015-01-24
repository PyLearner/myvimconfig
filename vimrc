if v:lang =~ "utf8$" || v:lang =~ "UTF-8$"
   set fileencodings=ucs-bom,utf-8,latin1
endif

set nocompatible	" Use Vim defaults (much better!)
set bs=indent,eol,start		" allow backspacing over everything in insert mode
"set ai			" always set autoindenting on
"set backup		" keep a backup file
set viminfo='20,\"50	" read/write a .viminfo file, don't store more
			" than 50 lines of registers
set history=50		" keep 50 lines of command line history
set ruler		" show the cursor position all the time
set nu




filetype off                   " required!



set rtp+=~/.vim/bundle/vundle/

call vundle#rc()



" let Vundle manage Vundle

" required!

Bundle 'gmarik/vundle'
Bundle 'majutsushi/tagbar'
Bundle 'nvie/vim-flake8'

" My Bundles here:

"

" original repos on github

Bundle 'scrooloose/syntastic'
Bundle 'davidhalter/jedi-vim'

Bundle 'scrooloose/nerdtree'

Bundle 'kien/ctrlp.vim'

"Bundle 'sjbach/lusty'

Bundle 'tpope/vim-fugitive'

Bundle 'vim-scripts/Syntastic'
Bundle 'nathanaelkane/vim-indent-guides'
Bundle 'jiangmiao/auto-pairs'


" vim-scripts repos

Bundle 'L9'



" non github repos

" Bundle 'git://git.wincent.com/command-t.git'



"

" Ò»Ð©»ù±¾ÅäÖÃ

"

filetype plugin indent on     " required!

let mapleader = ','

let g:mapleader = ','



" Ignore case when searching

set ignorecase

" When searching try to be smart about cases

set smartcase

" Highlight search results

set hlsearch

" Makes search act like search in modern browsers

set incsearch

" Use spaces instead of tabs

set expandtab



" Be smart when using tabs ;)

set smarttab

" 1 tab == 4 spaces

set shiftwidth=4

set tabstop=4

"Always show current position

set ruler

"

"" Height of the command bar

set cmdheight=2



set nobackup

set noswapfile

set nowb



" ×´Ì¬À¸ÅäÖÃ

set laststatus =2 "always has status line

set statusline=%F%m%r%h%w\ [TYPE=%Y]\ [POS=%04l,%04v]\ [%p%%]  

set statusline+=%=\ %{fugitive#statusline()}

set statusline+=%{SyntasticStatuslineFlag()}





"


"



" NERDTree=====

nmap <F2> :NERDTreeToggle<CR>

"nmap <F8> :TagbarToggle<CR>
nmap tb :Tagbar<cr>

let NERDTreeWinSize=22

let NERDTreeIgnore=['\.pyc', '\.swp']

"switch window

nnoremap <c-h> <c-w>h

nnoremap <c-j> <c-w>j

nnoremap <c-k> <c-w>k

nnoremap <c-l> <c-w>l



" LustyBufferExplorer=====

nnoremap <leader>lb :LustyBufExplorer<CR>

set hidden



"

" Brief help

" :BundleList          - list configured bundles

" :BundleInstall(!)    - install(update) bundles

" :BundleSearch(!) foo - search(or refresh cache first) for foo

" :BundleClean(!)      - confirm(or auto-approve) removal of unused bundles

"

" see :h vundle for more details or wiki for FAQ

" NOTE: comments after Bundle command are not allowed..




















" Only do this part when compiled with support for autocommands
if has("autocmd")
  augroup redhat
  autocmd!
  " In text files, always limit the width of text to 78 characters
  " autocmd BufRead *.txt set tw=78
  " When editing a file, always jump to the last cursor position
  autocmd BufReadPost *
  \ if line("'\"") > 0 && line ("'\"") <= line("$") |
  \   exe "normal! g'\"" |
  \ endif
  " don't write swapfile on most commonly used directories for NFS mounts or USB sticks
  autocmd BufNewFile,BufReadPre /media/*,/run/media/*,/mnt/* set directory=~/tmp,/var/tmp,/tmp
  " start with spec file template
  autocmd BufNewFile *.spec 0r /usr/share/vim/vimfiles/template.spec
  augroup END
endif

if has("cscope") && filereadable("/usr/bin/cscope")
   set csprg=/usr/bin/cscope
   set csto=0
   set cst
   set nocsverb
   " add any database in current directory
   if filereadable("cscope.out")
      cs add $PWD/cscope.out
   " else add database pointed to by environment
   elseif $CSCOPE_DB != ""
      cs add $CSCOPE_DB
   endif
   set csverb
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

filetype plugin on

if &term=="xterm"
     set t_Co=8
     set t_Sb=[4%dm
     set t_Sf=[3%dm
endif

" Don't wake up system with blinking cursor:
" http://www.linuxpowertop.org/known.php
let &guicursor = &guicursor . ",a:blinkon0"
"window position of nerdtree
let NERDTreeWinPos=1
"autocmd VimEnter * NERDTree
"tag bar
let tagbar_width=25

"jedi vim
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = "<leader>d"
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>r"
let g:jedi#show_call_signatures = "1"

"dui qi xian
let g:indent_guides_guide_size=1
"let g:indent_guides_auto_colors = 0
"autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=red   ctermbg=3
"autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=green ctermbg=4
"syntastic  configs

let g:syntastic_check_on_open=1
"let g:syntastic_enable_signs=1

"auto-pair
let g:AutoPairsFlyMode = 0
let g:AutoPairsShortcutBackInsert = '<M-b>'

"ctags
set tags=/internal_auto/tags
