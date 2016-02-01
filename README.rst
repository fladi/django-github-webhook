========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/django-github-webhook/badge/?style=flat
    :target: https://readthedocs.org/projects/django-github-webhook
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/fladi/django-github-webhook.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/fladi/django-github-webhook

.. |requires| image:: https://requires.io/github/fladi/django-github-webhook/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fladi/django-github-webhook/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/fladi/django-github-webhook/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fladi/django-github-webhook

.. |version| image:: https://img.shields.io/pypi/v/django-github-webhook.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/django-github-webhook

.. |downloads| image:: https://img.shields.io/pypi/dm/django-github-webhook.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/django-github-webhook

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-github-webhook.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/django-github-webhook

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/django-github-webhook.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/django-github-webhook

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/django-github-webhook.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/django-github-webhook


.. end-badges

A class based view for Django that can act as an receiver for GitHub webhooks. It is designed to validate all requests through their ``X-Hub-Signature``
headers.

Handling of GitHub events is done by implementing a class method with the same name as the event, e.g. ``ping``, ``push`` or ``fork``. See the documentation for
more in-depth information and examples.

* Free software: BSD license

Installation
============

::

    pip install django-github-webhook

Documentation
=============

https://django-github-webhook.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
