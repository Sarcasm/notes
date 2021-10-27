*****
CMake
*****

.. highlight:: cmake

.. contents::
   :local:


Introduction
============

List of CMake patterns/best practices.

These patterns are directed towards people writing the project CMake files,
but accounts for how the project CMake build
will be consumed by packagers or external developers.

The goals is to minimize the boilerplate for people writing the project CMake files,
and to maximize the portability and easy of use for packagers or external developers.


Compiler options
================

C++ standard
------------

Do's
~~~~

Set a minimum standard, not an exact standard.

Use ``target_compile_features(foo PUBLIC cxx_std_11)``
to specify the minimum standard your target requires:

- `cmake-commands(7) » target_compile_features <https://cmake.org/cmake/help/latest/command/target_compile_features.html>`_
- List of available standards in `cmake-properties(7) » CXX_STANDARD <https://cmake.org/cmake/help/latest/prop_tgt/CXX_STANDARD.html#prop_tgt:CXX_STANDARD>`_.

This allow a developer or packager to upgrade the standard seamlessly,
e.g. a packager may want to upgrade to C++20 for ABI-compatibility reasons.
This can be done by setting `CMAKE_CXX_STANDARD`_ from a toolchain file,
or from the command line:

.. code-block:: console

   $ cmake -DCMAKE_CXX_STANDARD=20 ...

CMake will also respect the ``-std=<standard>`` flag,
if specified specified from the environment variable ``CXXFLAGS``
(but this is read only during the initial project generation):

.. code-block:: console

   $ env CXXFLAGS=-std=c++20 cmake ...

or from the command line `CMAKE_CXX_FLAGS`_:

.. code-block:: console

   $ cmake -DCMAKE_CXX_FLAGS=-std=c++20 ...


When the compiler does not support the given standard,
CMake will generate an error during generation:

.. code-block:: console
   :emphasize-lines: 8-14

   $ cmake ..
   -- The CXX compiler identification is GNU 4.8.5
   -- Detecting CXX compiler ABI info
   -- Detecting CXX compiler ABI info - done
   -- Check for working CXX compiler: /usr/bin/c++ - skipped
   -- Detecting CXX compile features
   -- Detecting CXX compile features - done
   CMake Error at CMakeLists.txt:55 (target_compile_features):
     target_compile_features The compiler feature "cxx_std_17" is not known to
     CXX compiler

     "GNU"

     version 4.8.5.


   -- Configuring incomplete, errors occurred!
   See also "/root/app/build/CMakeFiles/CMakeOutput.log".
   See also "/root/app/build/CMakeFiles/CMakeError.log".


In CI, to make sure the minimum C++ standard is actually tested,
set it explicitely using one of the aforementioned methods.


Don'ts
~~~~~~
(don't) set `CMAKE_CXX_STANDARD`_ in a CMakeLists.txt:

- It is targeted to toolchain files users,
  for packagers/developers that want to use a specific version.

  See https://gitlab.kitware.com/cmake/cmake/issues/17146#note_299405.

- It will not be propagated to downstream targets.

See also
~~~~~~~~

- https://cmake.org/cmake/help/latest/manual/cmake-compile-features.7.html#requiring-language-standards

.. _CMAKE_CXX_STANDARD: https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html
.. _CMAKE_CXX_FLAGS: https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_FLAGS.html

Optional dependencies
=====================

Third party or platform-specific integrations
are useful to represent as optional dependencies.

As someone who wants to quick-test a project,
having interest in the core of the project,
I prefer to have the optional dependencies auto-detected
so that I can get started without being encombered by build issues
or having to install system packages:

.. code-block:: console

   $ mkdir build
   $ cd build
   $ cmake ..

As a packager, or as a developer working on the optional feature,
I want control of the detection,
so that I can make sure the project works with (or without) it:

.. code-block:: console

   $ mkdir build
   $ cd build
   $ cmake -DWITH_FOO=ON ..


The pattern
-----------

Declare an option ``WITH_${INTEGRATION}`` with 3 possible value:
``AUTO`` (the default), ``ON`` and ``OFF``::

   set(WITH_JOURNALD "AUTO" CACHE STRING
     "Whether or not to support journald logging (this feature requires the systemd development package)")
   set_property(CACHE WITH_JOURNALD PROPERTY STRINGS AUTO ON OFF)

Thanks to the use of
`cmake-properties(7) » STRINGS <https://cmake.org/cmake/help/latest/prop_cache/STRINGS.html>`_,
the CMake UIs will complete the possible values,
which is nice for discoverability:

- ``ccmake`` will cycle through the values when hitting ``Enter``.
- ``cmake-gui`` will show a combo box:

  .. image:: cmake/option-auto-cmake-gui-combobox.png
     :scale: 50%
     :alt: cmake-gui combo box screenshot

Later on, when resolving dependencies::

   if (WITH_JOURNALD STREQUAL "AUTO")
      pkg_check_modules(libsystemd IMPORTED_TARGET libsystemd)
      # shadow origin value with ON/OFF,
      # so journald-specific code just has to check:
      #     if (WITH_JOURNALD)
      #         ...
      #     endif()
      if (libsystemd_FOUND)
        set(WITH_JOURNALD ON)
      else()
        set(WITH_JOURNALD OFF)
      endif()
    elseif (WITH_JOURNALD)  # ON
      pkg_check_modules(libsystemd REQUIRED IMPORTED_TARGET libsystemd)
    endif()

After we checked the special value ``AUTO``,
we shadow the variable with a boolean value.

From now on, you can consider this option a boolean,
check it with ``if (WITH_JOURNALD)``, example::

    if (WITH_JOURNALD)
        set_property(
          SOURCE src/log_backends.cpp
          APPEND PROPERTY COMPILE_DEFINITIONS WITH_JOURNALD
        )

      target_link_libraries(foo PRIVATE PkgConfig::libsystemd)
    endif()

All the CMake boolean values are also supported, not just ``ON/OFF``,
e.g. ``-DWITH_JOURNALD=YES``, ``-DWITH_JOURNALD=0``, ``-DWITH_JOURNALD=TRUE``.

This means it is safe to use replace boolean options like
`option(WITH_JOURNALD, "...") <https://cmake.org/cmake/help/latest/command/option.html>`_
to support this new ``AUTO`` value in a backward compatible way,
without breaking packagers explicit configurations.
