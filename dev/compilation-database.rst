
********************
Compilation database
********************

.. contents::
   :local:


What is a compilation database?
===============================

A compilation database is a database for compile options.
It records which compile options are used to build the files in a project.
A compilation database can be, but is not limited to,
a `JSON Compilation Database`_.
Refer to the `clang::tooling::CompilationDatabase`_ class
for the full interface.

A real-world JSON Compilation Database *entry* looks like this:

.. code-block:: json

    {
      "directory": "/home/user/dev/llvm/build",
      "command": "/usr/bin/clang++   -DGTEST_HAS_RTTI=0 -D_DEBUG -D_GNU_SOURCE -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -Ilib/Support -I/home/user/dev/llvm/llvm/lib/Support -Iinclude -I/home/user/dev/llvm/llvm/include   -fPIC -fvisibility-inlines-hidden -Wall -W -Wno-unused-parameter -Wwrite-strings -Wcast-qual -Wmissing-field-initializers -pedantic -Wno-long-long -Wcovered-switch-default -Wnon-virtual-dtor -Wdelete-non-virtual-dtor -Werror=date-time -std=c++11 -fcolor-diagnostics -ffunction-sections -fdata-sections -O3    -UNDEBUG  -fno-exceptions -fno-rtti -o lib/Support/CMakeFiles/LLVMSupport.dir/APFloat.cpp.o -c /home/user/dev/llvm/llvm/lib/Support/APFloat.cpp",
      "file": "/home/user/dev/llvm/llvm/lib/Support/APFloat.cpp"
    }


.. note:: A good introduction to compilation databases
          is available on Eli Bendersky's blog:

          * `Compilation databases for Clang-based tools`_


What is it good for?
====================

You might wonder what a compilation database is good for.
This section list a various tools that may benefit from a compilation database.


Clang tools
-----------

`Core Clang tools`_ and `extra Clang tools`_:

* `clang-check <http://clang.llvm.org/docs/ClangCheck.html>`_
* `clang-include-fixer <http://clang.llvm.org/extra/include-fixer.html>`_
* `clang-rename <http://clang.llvm.org/extra/clang-rename.html>`_
* `clang-tidy <http://clang.llvm.org/extra/clang-tidy>`_


A few other tools seems to be available,
but they aren't officially documented:

* ``clang-reorder-fields``
* ``clang-change-namespace``
* ``clang-move``

It's possible these tools will be merged into one,
be it called ``clang-refactor`` or not.

.. seealso::

   * Some of these tools are demoed in the following blog post:
     `Improving workflow by using Clang-based tools
     <https://omtcyfz.github.io/2016/08/30/Improving-workflow-by-using-Clang-based-tools.html>`_

   * `clang-refactor's design document
     <https://docs.google.com/document/d/1w9IkR0_Gqmd5w4CZ2t_ZDZrNLYVirQPyMS41533HQZE/edit?usp=sharing>`_

   * ``clang-refactor`` state is undefined at this point:

       "As you can see, the project scale is just huge. I started it as an intern
       this summer, but now I got back to studies and therefore I can't work on
       that extensively at least until the next summer.

       However, as far as I understand my former team was interested in the
       project and there is a decent chance they'll continue my work,
       I'll be happy if they do."

       -- https://www.reddit.com/r/cpp/comments/59n8ya/what_happened_to_clang_server/d9a2xi3/


Text editors and IDEs
---------------------

To bring basic IDE-like features to text editor you need 2 things:

1. text editor plugin which integrates libclang_
2. a compilation database, to feed to libclang_

With this, you can have features such as semantic code completion
and on-the-fly syntax checking.


GNU Emacs
^^^^^^^^^

* https://github.com/abingham/emacs-ycmd
* https://github.com/Andersbakken/rtags
* https://github.com/kumar8600/flycheck-clangcheck
* https://github.com/randomphrase/ede-compdb
* https://github.com/Sarcasm/irony-mode


Vim
^^^

* http://valloric.github.io/YouCompleteMe
* https://github.com/Rip-Rip/clang_complete
* https://github.com/jeaye/color_coded


Other tools
-----------

* With little effort the Kythe_ indexer can be run on a compilation database.

* Your your own tool based on Clang's LibTooling_.

* `PVS-Studio on Linux <http://www.viva64.com/en/m/0036/>`_ [#pvs-studio-linux-compdb]_

* `cc_driver.pl`_ from the `Mo' Static <http://btorpey.github.io/blog/2016/04/07/mo-static/>`_
  article.

.. seealso::

   Some of the tools listed here:

   * http://clang.llvm.org/docs/ExternalClangExamples.html


How to generate a JSON Compilation Database?
============================================

.. contents::
   :local:


Build system
------------

This section describes build tools which natively support
the generation of a compilation database.

CMake
^^^^^

To generate a JSON compilation database with CMake_,
enable the `CMAKE_EXPORT_COMPILE_COMMANDS`_ option
(requires ``CMake >= 2.8.5``).

For example, in an existing build directory, type::

  cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .

This will create a file name ``compile_commands.json`` in the build directory.


Ninja
^^^^^

To generate a JSON compilation database with Ninja_,
use the `-t compdb`_ option (requires ``Ninja >= 1.2``).
This option takes a list of rules as argument.

Usage::

  ninja -t compdb [RULES...]

This works well with projects containing one rule for C++ files,
such as Ninja_ itself::

  ninja -t compdb cxx > compile_commands.json

However, it gets ugly if the Ninja build files contains a lot of rules.
You have to find a way to get a list of all the rules.
For example,
as of version 3.6.1,
CMake generates a lot of rules.
To generate a compilation database of Clang using CMake's Ninja generator
(``cmake -G Ninja <...>``)::

  ninja -t compdb $(awk '/^rule (C|CXX)_COMPILER__/ { print $2 }' rules.ninja) > compile_commands.json

This method is not ideal,
the ``awk`` line is not really good parser for Ninja syntax.
To make things better,
there is an issue on the ninja bug tracker with an associated pull request:

* https://github.com/ninja-build/ninja/issues/1024
* https://github.com/ninja-build/ninja/pull/1025


Specialized tools
-----------------

Some build systems do not support generating a compilation database.

A non-exhaustive list, includes:

* the GNU Build System (autotools): ``./configure`` and friends
* KBuild, the Linux Kernel Makefiles

For this reason, a few tools have emerged to respond to this issue.


bear and intercept-build
^^^^^^^^^^^^^^^^^^^^^^^^

Bear_ and `intercept-build` from scan-build_,
are two tools from `László Nagy`_,
that collects the compile options by intercepting calls to the compiler
during the build.
To have a complete compilation database a full build is required.

The scan-build_ tools is included in Clang tree since release 3.8.0,
as a replacement of the Perl implementation of ``scan-build``.
It's reasonable to think that someday, distributions will offer it as package.
``scan-build`` can already be easily be installed with pip_::

  pip install scan-build

Usage::

  <bear|intercept-build> BUILD_COMMAND

Example::

  bear make -B -j9
  intercept-build ./build.sh

A file named ``compile_commands.json`` is created in the current directory.


compdb
^^^^^^

compdb_ is a tool to manipulate compilation databases.
It can generate a compilation database for header files.


sw-btrace
^^^^^^^^^

sourceweb_\ 's btrace_ tool, aka ``sw-btrace``, use the same principle as `bear and intercept-build`_.

The generation is done in 2 steps:

1. Run ``sw-btrace BUILD_COMMAND`` to log the compilation.
2. Call ``sw-btrace-to-compiledb`` to generate a JSON compilation database
   out of the compilation log.

Example::

  sw-btrace make -B
  sw-btrace-to-compiledb

A file named ``compile_commands.json`` is created in the current directory.


xcpretty
^^^^^^^^

xcpretty_ can generate a compilation database for Xcode projects.
To do so, it uses the ``xcodebuild`` output.

Usage::

    xcodebuild | xcpretty -r json-compilation-database


Other compilation databases and tools
=====================================

This section shows that people invented their own compilation database version.
Either because no standards existed yet, or because of specialized needs.


cc_args.py
----------

The `cc_args.py`_ script
from the Vim plugin `clang_complete
<https://github.com/Rip-Rip/clang_complete>`_.

This script generates a `.clang_complete
<https://github.com/Rip-Rip/clang_complete/blob/c7f5673a5d31704e9ec43d43c0606b243d5ef623/doc/clang_complete.txt#L59-L87>`_
configuration file.

Usage::

  make CC='~/.vim/bin/cc_args.py gcc' CXX='~/.vim/bin/cc_args.py g++' -B


gccrec
------

The ``gccrec`` tool from the now unmaintained `gccsense
<https://github.com/m2ym/gccsense>`_ project.

The tool records the compile options in an SQLite database.

Links to the manual for reference:

* `txt <https://github.com/m2ym/gccsense/blob/67c76de401b3d11ccbba0e6d782c8686a341aabf/doc/manual.txt#L205-L252>`_
* `HTML <https://web.archive.org/web/20150223192059/http://cx4a.org/software/gccsense/manual.html#gccrec>`_


rtags
-----

The rtags_ project has a gcc wrapper named ``gcc-rtags-wrapper.sh``
to help feed its internal compilation database.

Description here:

* https://github.com/Andersbakken/rtags/#setup


YCM-Generator
-------------

YCM-Generator_ works differently than `bear and intercept-build`_.
It builds a project using a *fake toolchain*.
This is faster than doing a full build,
because the fake toolchain is composed of trivial programs.

The tool does not actually generate a "JSON Compilation Database",
instead it creates a configuration file for YouCompleteMe_.


Case studies on a few open source projects
==========================================

This section describes how to generate a compilation database
for a few open source projects.
Depending on the project,
the method to generate a compilation database can differ.

The result should preferrably be:

**correct**
  Some tools guess the compile options,
  if they guess wrong, the compile command entry is not useful.

**complete**
  A compilation database should be as exhaustive as possible.
  Any file on which a tool can be run on, need to have compile options.

  For example, a compilation database usually lacks compile options for headers,
  even though they would be useful to things like text editors.
  Or compile options for unit tests may not be available,
  if tests aren't built by default.

**fast**
  Between 2 or more correct and complete methods, one should favor the fastest.

  Tools that require a full project build to generate the database
  can easily become a hindrance on big projects.
  Imagine adding a new file to a big project.
  When you have to do a full rebuild
  just to make the file show up in the database,
  it's not pleasant.


git
---

git_ uses a custom Makefile and a ``configure`` scripts for the build.
The build system does not seem to have native support
for the compilation database generation.
We will use `bear and intercept-build`_ to generate one.

From a quick glimpse at the Makefile and documentation,
we can see there is a special ``DEVELOPER`` setting
to enable stricter compilation options.
This is used in this example to match the developer workflow better.

This example has been tested on git 2.9.2.

Compilation database generation with ``bear``::

  echo DEVELOPER=1 >> config.mak
  make configure
  bear make -j9

With ``intercept-build``, replace the last line by::

  intercept-build make -j9


.. rubric:: Footnotes

.. [#pvs-studio-linux-compdb] http://www.viva64.com/en/b/0446/#ID0EEAAC


.. _JSON Compilation Database: http://clang.llvm.org/docs/JSONCompilationDatabase.html
.. _`clang::tooling::CompilationDatabase`: http://clang.llvm.org/doxygen/classclang_1_1tooling_1_1CompilationDatabase.html
.. _Compilation databases for Clang-based tools: http://eli.thegreenplace.net/2014/05/21/compilation-databases-for-clang-based-tools
.. _libclang: http://clang.llvm.org/doxygen/group__CINDEX.html
.. _Core Clang tools: http://clang.llvm.org/docs/ClangTools.html
.. _extra Clang tools: http://clang.llvm.org/extra/index.html
.. _Kythe: https://www.kythe.io
.. _LibTooling: http://clang.llvm.org/docs/LibTooling.html
.. _cc_driver.pl: http://btorpey.github.io/pages/cc_driver.pl/index.html
.. _CMake: https://cmake.org
.. _CMAKE_EXPORT_COMPILE_COMMANDS: https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html
.. _Ninja: https://ninja-build.org
.. _-t compdb: https://ninja-build.org/manual.html#_extra_tools
.. _Bear: https://github.com/rizsotto/Bear
.. _scan-build: https://github.com/rizsotto/scan-build
.. _László Nagy: https://github.com/rizsotto
.. _pip: https://pip.pypa.io/en/stable/
.. _YCM-Generator: https://github.com/rdnetto/YCM-Generator
.. _YouCompleteMe: https://github.com/Valloric/YouCompleteMe
.. _rtags: https://github.com/Andersbakken/rtags
.. _sourceweb: https://github.com/rprichard/sourceweb
.. _btrace: https://github.com/rprichard/sourceweb#btrace
.. _xcpretty: https://github.com/supermarin/xcpretty
.. _compdb: https://github.com/Sarcasm/compdb
.. _git: https://git-scm.com/
