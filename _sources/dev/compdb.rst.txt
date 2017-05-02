
******
compdb
******

.. contents::
   :local:


Release procedure
=================

Clone latest Github release to a new ``compdb-dist`` directory::

  git clone git@github.com:Sarcasm/compdb.git compdb-dist
  cd compdb-dist


Increment version
-----------------

Increment version in ``compdb/__about__.py``.


Run tests
---------

Run test suite::

  tox --skip-missing-interpreters

README validation for PyPI::

  python setup.py --long-description | rst2html.py > /tmp/output.html
  chromium /tmp/output.html

Install locally for following tests::

  rm -rf .venv-release
  virtualenv .venv-release
  source .venv-release/bin/activate
  pip install -r requirements.txt

Regression tests::

  source .venv-release/bin/activate
  pushd tests/regression/headerdb
  make clean
  make all
  popd

Packaging tests (requires Docker)::

  ./tests/integration/docker/ubuntu-trusty.sh \
      tests/integration/packaging-trusty.sh

Contrib scripts::

  source .venv-release/bin/activate
  ./contrib/zsh/check-all-helps


Make git tag
------------

.. code-block:: bash

   COMPDB_VERSION=$(python compdb version --short)
   echo "tagging $COMPDB_VERSION"
   git tag -a v$COMPDB_VERSION -m "compdb $COMPDB_VERSION"
   git push --follow-tags

Notes:

- Use annotated tags, lightweight tags aren't appropriate for releases,
  they are for local development.
  Annotated tags can have author, date and message.
  They are shown by default when using ``git describe``,
  that is not the case for lightweight tags.
  However, regarding the message, it seems a bit useful,
  at least the way it is used by many projects in the wild:
  "version X.Y.Z", "project X.Y.Z", "X.Y.Z", ...
  It could make sense to use an empty message ``-m ''``.
  Alternatively they could be use to contain the release notes
  but there are no official format (e.g. Markdown),
  so this may better be in the project's documentation.
  On Github, release notes, have to be written manually anyway:

  - https://github.com/Sarcasm/compdb/releases

- Using ``--follow-tags`` will only push annotated tags,
  that are reacheable (an ancestor) from the pushed commits.

- Potential improvement, sign releases:

  - https://github.com/flycheck/flycheck/blob/424a78328518e1dabf830f792ce9c4aa1ff7fc7e/doc/contributor/maintaining.rst#signatures-for-commits-and-tags

Make pretty release note on Github release page:

- https://github.com/Sarcasm/compdb/releases/


Publish on Pypi
---------------

One time configuration,
steps to do again only if the release environment changes.

Create a ``~/.pypirc`` with this content:

.. code-block:: ini

  [distutils]
  index-servers=pypi

  [pypi]
  username = Sarcasm
  EOF


Make sure to remove any resident packages::

   rm -rf dist/*

Build source distribution and universal wheel::

  source .venv-release/bin/activate
  pip install wheel
  python setup.py sdist bdist_wheel

Upload packages::

  source .venv-release/bin/activate
  pip install twine
  twine upload dist/*
