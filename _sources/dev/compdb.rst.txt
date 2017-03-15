
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

  virtualenv .venv
  source .venv/bin/activate
  pip install -r requirements.txt

Regression tests::

  source .venv/bin/activate
  cd tests/regression/headerdb
  make all

Contrib scripts::

  source .venv/bin/activate
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


Install dependencies::

  source .venv/bin/activate
  pip install wheel
  pip install twine

Build the distribution::

  python setup.py sdist bdist_wheel
  twine upload dist/*
