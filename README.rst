=====================
The Campaigns Library
=====================

Development setup
=================

It's recommended you use `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_
and `The Developer Society Dev Tools <https://github.com/developersociety/tools>`_.

Presuming you are using those tools, getting started on this project is pretty straightforward:

.. code:: console

    $ dev-clone commonslibrary
    $ workon commonslibrary
    $ make reset

You can now run the development server:

.. code:: console

    $ python manage.py runserver
