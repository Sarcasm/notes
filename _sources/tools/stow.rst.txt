
********
GNU Stow
********

.. contents::
   :local:


Introduction
============

I use `GNU Stow`_ to install locally the latest version
of a handful of open source projects I care about.

I also use it to manage my dotfiles:

* https://github.com/Sarcasm/dotfiles

This page is a memo about the usage I make of the tool.


Filesystem layout
=================

I install my packages in ``~/pkg/stow/<package[-version]>``.

``~/pkg/bin`` is added to the ``PATH``,
it precedes the system binaries' search paths.

``~/.profile`` excerpt::

    # User's Stow packages
    if [ -d "$HOME/pkg/bin" ]; then
        PATH="$HOME/pkg/bin:$PATH"
    fi


General cooking recommendations
===============================

The official recommendations are available in the manual:

* https://www.gnu.org/software/stow/manual/html_node/Compile_002dtime-vs-Install_002dtime.html

This link also explains why it is necessary sometimes
to make the package believe it is installed to ``~/pkg``
and not ``~/pkg/stow/<package>``.


CMake
-----

Generic recipe::

  cmake -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/pkg/stow/<package> <args...>
  ninja
  ninja install
  cd ~/pkg/stow
  stow <package>


GNU Build System
----------------

Generic recipe::

  configure --prefix=$HOME/pkg <args...>
  make
  make install prefix=$HOME/pkg/stow/<package>
  cd ~/pkg/stow
  stow <package>

.. seealso::

   * https://www.gnu.org/software/stow/manual/stow.html#Other-FSF-Software


Troubleshooting
---------------

Some packages do not only add new files,
but sometimes update some files.

GNU Info for example, has an index file in ``share/info/dir``.

Emacs and mu4e conflicts on this, example::

  $ stow emacs-25.1-rc2
  WARNING! stowing emacs-25.1-rc2 would cause conflicts:
    * existing target is stowed to a different package: share/info/dir => ../../stow/mu/share/info/dir
  All operations aborted.
  $

To get rid of the issue::

  $ cat <<'EOF' > .stowrc
  --ignore=share/info/dir
  EOF

.. seealso::

   * https://www.gnu.org/software/stow/manual/stow.html#Perl-and-Perl-5-Modules
   * ``perllocal.pod`` example:
     https://www.gnu.org/software/stow/manual/stow.html#Resource-Files

Recipes
=======

ag
---

* https://github.com/ggreer/the_silver_searcher

Import public key (http://geoff.greer.fm/ag/)::

    gpg --import ggreer_gpg_key.asc

Debian prerequisites::

  sudo apt-get install automake pkg-config libpcre3-dev zlib1g-dev liblzma-dev

Recipe::

  gpg --verify the_silver_searcher-0.32.0.tar.gz.asc
  tar xaf the_silver_searcher-0.32.0.tar.gz
  ./configure --prefix=$HOME/pkg
  make
  make install prefix=$HOME/pkg/stow/ag-0.32.0
  cd ~/pkg/stow/
  stow ag-0.32.0


emacs
-----

Download: https://www.gnu.org/software/emacs/download.html

I don't think the instructions from the manual are still relevant,
it seems they were written for Emacs 19.31,
but it might be a good idea to check if that changed:

* https://www.gnu.org/software/stow/manual/stow.html#GNU-Emacs

  Since the 24.5 release,
  tarballs are signed with the GPG key from Nicolas Petton ``7C207910``,
  fingerpint ``28D3 BED8 51FD F3AB 57FE F93C 2335 87A4 7C20 7910``,
  which can be found in the GNU keyring.

  -- https://www.gnu.org/software/emacs/download.html

Get GPG key::

  gpg --keyserver hkp://keys.gnupg.net --recv-keys 7C207910


Recipe::

  gpg --verify emacs-25.1-rc2.tar.xz.sig
  unxz emacs-25.1-rc2.tar.xz
  tar xaf emacs-25.1-rc2.tar
  mkdir emacs-25.1-build
  cd emacs-25.1-build
  # install necessary dependencies (e.g: apt-get install build-dep emacs24)
  # enable module support,
  # xwidget (requires libwebkitgtk-3.0-dev ubuntu, webkitgtk arch)
  ../emacs-25.1/configure --with-modules --with-xwidgets --prefix=$HOME/pkg/
  make -j9
  make prefix=$HOME/pkg/stow/emacs-25.1-rc2 install
  cd ~/pkg/stow
  stow emacs-25.1-rc2


git
---

Download: https://www.kernel.org/pub/software/scm/git/

Build instructions: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git#Installing-from-Source

Recipe::

  gpg --keyserver hkp://keys.gnupg.net --recv-keys 96AFE6CB
  unxz git-2.9.2.tar.xz
  gpg --verify git-2.9.2.tar.sign
  tar xaf git-2.9.2.tar
  cd git-2.9.2
  # install necessary dependencies (zlib, ssl, ...), e.g: using apt-get build-dep git
  make configure
  ./configure --prefix=$HOME/pkg/stow/git-2.9.2
  make all doc info -j9
  make install install-doc install-info
  cd ~/pkg/stow
  stow git-2.9.2


mu4e
----

* http://www.djcbsoftware.nl/code/mu/mu4e/Installation.html#Installation

Recipe::

  git clone git://github.com/djcb/mu.git
  env CC=clang CXX=clang++ autoreconf -i
  env CC=clang CXX=clang++ ./configure --prefix=$HOME/pkg
  make -j9
  make install prefix=$HOME/pkg/stow/mu
  cd ~/pkg/stow
  stow mu

Emacs Configuration::

  (add-to-list 'load-path "~/pkg/share/emacs/site-lisp/mu4e")


repo
----

* https://source.android.com/source/downloading.html

Recipe::

  mkdir -p ~/pkg/stow/repo/bin
  wget 'https://storage.googleapis.com/git-repo-downloads/repo' -O ~/pkg/stow/repo/bin/repo
  chmod a+x ~/pkg/stow/repo/bin/repo
  cd ~/pkg/stow
  stow repo


sourceweb
---------

* https://github.com/rprichard/sourceweb

``make install prefix=<path>`` is not satisfied like,
however it is not an issue for this program
to be installed in the ``~/pkg/stow/<package>`` directory.

Recipe::

  ./configure --prefix=$HOME/pkg/stow/sourceweb
  make
  make install
  cd ~/pkg/stow
  stow sourceweb


.. Links

.. _GNU Stow: https://www.gnu.org/software/stow
