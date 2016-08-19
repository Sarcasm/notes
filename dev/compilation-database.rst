
********************
Compilation database
********************

.. contents::
   :local:
   :depth: 2


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

You might wonder what a compilation database is good for?

It can be useful to:

* Text editors and IDEs, to provide more insight to the code.
  For example on-the-fly syntax checking, completions, disassembly view.
* `core Clang tools`_ and `extra Clang tools`_, such as clang-tidy_.
* Other external tools, whether they are based on Clang or not.

.. seealso:: A good introduction to compilation databases
             is available on Eli Bendersky's blog:

             * `Compilation databases for Clang-based tools`_


Build tools
===========

This section describes build tools which natively support
the generation of a compilation database.

CMake
-----

To generate a JSON compilation database with CMake_,
enable the `CMAKE_EXPORT_COMPILE_COMMANDS`_ option.

For example, in an existing build directory, type::

  cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .

This will create a file name ``compile_commands.json`` in the build directory.


Other tools
===========

Some build systems do not support generating a compilation database.

A non-exhaustive list, includes:

* the GNU Build System (autotools): ``./configure`` and friends
* KBuild, the Linux Kernel Makefiles

For this reason, a few tools have emerged to respond to this issue.


bear and intercept-build
------------------------

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
------

compdb_ is a versatile tool to manipulate compilation databases.
It can for example generate a compilation database for header files.


sw-btrace
---------

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
--------

xcpretty_ can generate a compilation database for Xcode projects.
To do so, it uses the ``xcodebuild`` output.

Usage::

    xcodebuild | xcpretty -r json-compilation-database


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

* **correct**

  Some tools guess the compile options,
  if they guess wrong, the compile command entry is not useful.

* **complete**

  A compilation database should be as exhaustive as possible.
  Any file on which a tool can be run on, need to have compile options.

  For example, a compilation database usually lacks compile options for headers,
  even though they would be useful to things like text editors.
  Or compile options for unit tests may not be available,
  if tests aren't built by default.

* **fast**

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

  intercept-build --override-compiler make -j9

.. note::

  I'm not sure why ``--override-compiler`` is needed.
  Not using it results in a crash.
  This is using scan-build version 1.1.


.. _JSON Compilation Database: http://clang.llvm.org/docs/JSONCompilationDatabase.html
.. _`clang::tooling::CompilationDatabase`: http://clang.llvm.org/doxygen/classclang_1_1tooling_1_1CompilationDatabase.html
.. _clang-tidy: http://clang.llvm.org/extra/clang-tidy
.. _Compilation databases for Clang-based tools: http://eli.thegreenplace.net/2014/05/21/compilation-databases-for-clang-based-tools
.. _core Clang tools: http://clang.llvm.org/docs/ClangTools.html
.. _extra Clang tools: http://clang.llvm.org/extra/index.html
.. _CMake: https://cmake.org
.. _CMAKE_EXPORT_COMPILE_COMMANDS: https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html
.. _Bear: https://github.com/rizsotto/Bear
.. _scan-build: https://github.com/rizsotto/scan-build
.. _László Nagy: https://github.com/rizsotto
.. _pip: https://pip.pypa.io/en/stable/
.. _YCM-Generator: https://github.com/rdnetto/YCM-Generator
.. _YouCompleteMe: https://github.com/Valloric/YouCompleteMe
.. _sourceweb: https://github.com/rprichard/sourceweb
.. _btrace: https://github.com/rprichard/sourceweb#btrace
.. _xcpretty: https://github.com/supermarin/xcpretty
.. _compdb: https://github.com/Sarcasm/compdb
.. _git: https://git-scm.com/
