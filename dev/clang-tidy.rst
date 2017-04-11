
**********
Clang-Tidy
**********

.. contents::
   :local:


If you don't know what clang-tidy is, read the overview here:

* http://clang.llvm.org/extra/clang-tidy/


Identifier naming
=================

The readability-identifier-naming_ check ensures the identifiers matches the
coding style of the project.
The naming convention can be specified in the ``.clang-tidy`` configuration
file.

This check is complementary to clang-format_
but it requires more effort to run
as it needs to know the compile options for the file.

.. _readability-identifier-naming: http://clang.llvm.org/extra/clang-tidy/checks/readability-identifier-naming.html
.. _clang-format: http://clang.llvm.org/docs/ClangFormat.html


Below is a sample configuration demonstrating a few kind of identifiers
and some possible values.
In this example,
classes and structs are ``CamelCase``,
variables and functions are ``lower_case``,
private members start with ``m_``, etc.

.. code-block:: yaml

    Checks: '-*,readability-identifier-naming'
    CheckOptions:
      - { key: readability-identifier-naming.NamespaceCase,       value: lower_case }
      - { key: readability-identifier-naming.ClassCase,           value: CamelCase  }
      - { key: readability-identifier-naming.PrivateMemberPrefix, value: m_         }
      - { key: readability-identifier-naming.StructCase,          value: CamelCase  }
      - { key: readability-identifier-naming.FunctionCase,        value: lower_case }
      - { key: readability-identifier-naming.VariableCase,        value: lower_case }
      - { key: readability-identifier-naming.GlobalConstantCase,  value: UPPER_CASE }

Here is a self-contained example to try ``clang-tidy`` out::

  mkdir /tmp/tidy-test
  cd  /tmp/tidy-test
  cat <<'EOF' > test.cpp
  class foo
  {
  public:
    foo() = default;

  private:
    int bar_;
  };
  EOF
  clang-tidy -checks='-*,readability-identifier-naming' \
      -config="{CheckOptions: [ {key: readability-identifier-naming.ClassCase, value: CamelCase} ]}" \
      test.cpp -- -std=c++11

See also
--------

* List of available identifiers:
  `clang-tidy/readability/IdentifierNamingCheck.cpp
  <https://github.com/llvm-mirror/clang-tools-extra/blob/8eb332109a2c68f791eda33fe28f174e77bbc5fe/clang-tidy/readability/IdentifierNamingCheck.cpp#L66>`_


CMake integration
=================

Since CMake 3.6 [#cmake-3.6-release]_,
it is possible to run ``clang-tidy`` as a part of the build.
This can be done on a per-target basis,
but if you don't want to modify the project's ``CMakeLists.txt``, 
it is possible to enable ``clang-tidy`` for the whole project
by using the CMake variable `CMAKE_<LANG>_CLANG_TIDY`_.

Please note that, ``clang-tidy`` arguments should be a CMake list,
each argument separated by ``;`` on the command line.

.. _CMAKE_<LANG>_CLANG_TIDY: https://cmake.org/cmake/help/latest/prop_tgt/LANG_CLANG_TIDY.html#prop_tgt:<LANG>_CLANG_TIDY

To use ``clang-tidy`` on a C++ project, type::

  mkdir tidy-build
  cd tidy-build
  CC=clang CXX=clang++ cmake \
      -DCMAKE_CXX_CLANG_TIDY="clang-tidy;-warnings-as-errors=*;-header-filter=$(realpath ..)" \
      ..
  make -k

This invocation is made uses ``-warnings-as-errors=*``,
this can be useful for continuous integration systems.
The return code of ``clang-tidy`` is handled
since CMake 3.8 [#cmake-3.8-release]_,
so this won't work with the CMake 3.6 and 3.7 series.


What's wrong with the CMake integration?
----------------------------------------

- Constant overhead for compilation in developement.

  For developement linting is nice before committing,
  but not necessarily when iterating on the code.

- If you want to modernize/fix your code,
  you need another way to run clang-tidy anyway.

  Clang has two scripts for example:

  1. ``run-clang-tidy.py``: useful to run clang-tidy on a compilation database
  2. ``clang-tidy-diff.py``: useful to run clang-tidy on a diff output

  CMake is still useful to generate the compilation database the tool runs on.

- No way to force colors.

  This may actually be a missing feature in ``clang-tidy``,
  which lacks something like ``-fdiagnostic-colors``.

.. todo::

   * Check MSVC compability mode (clang-cl).

     It may possible to work by using ``clang-cl`` compatible flags like this::

       cmake -DCMAKE_CXX_CLANG_TIDY="clang-tidy;-header-filter=$(realpath ..);-fms-extensions;-fms-compatibility-version=19;-D_M_AMD64=100" ..

     Idea from reddit/r/cpp:

     * https://www.reddit.com/r/cpp/comments/5b397d/what_c_linter_do_you_use/d9lvjiv/

.. rubric:: Footnotes

.. [#cmake-3.6-release] https://cmake.org/cmake/help/v3.6/release/3.6.html
.. [#cmake-3.8-release] https://cmake.org/cmake/help/v3.8/release/3.8.html
