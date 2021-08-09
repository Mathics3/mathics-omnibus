|Pypi Installs| |Latest Version| |Supported Python Versions|

Mathics is a general-purpose computer algebra system (CAS). It is an open-source alternative to Mathematica. It is free both as in "freedom" and as in "free beer".

`Mathics <https://mathics.org>`_ consists of a number of separable components so that those pieces that are desired can be used without the burden of dependencies of the other parts.

For example if you are interested in just running a command-line interface, you might not be interested in having Django and what that entails and vice versa.
If you are just interested in the computational library, there is no need for either the Web parts or the command-line library parts.

But what if you want both command-line interface, Web interface, all of the Pymathics libraries and whatever else there is to offer?

That's what this repository is about. Here we have a PyPI installable package that pull in the various components and offer commands:

* ``mathicsscript`` to run the command-line interface,
* ``mathicsserver`` to run the Django-Web server,
* ``dmathicsscript`` and ``dmathicsserver`` which runs the docker version of these,
* ``dmathicssdoc`` which runs a PDF viewer, `evince <https://wiki.gnome.org/Apps/Evince>`_, which can view the generated reference manual in PDF.
* ``dmathicsdoccopy`` which copies the the generated reference PDF manual out of the container and into the host filesystem.

This repository also contains the Dockerfiles used to create the `mathicsorg/mathics docker images <https://hub.docker.com/repository/docker/mathicsorg/mathics>`_.

That image is a combination of:

* `Mathics-Scanner <https://github.com/Mathics3/mathics-scanner>`_ (WL Character Tables and Mathics Scanner)
* `mathicsscript <https://github.com/Mathics3/mathicsscript>`_ (Command-line Mathics Interface)
* `mathics-pygments <https://github.com/Mathics3/mathics-pygments>`_ (WL Syntax Highlighting)
* `Mathics-Django <https://github.com/Mathics3/Mathics-Django>`_ (Django-based HTTP server)
* `mathics-threejs-backend <https://github.com/Mathics3/mathics-threejs-backend>`_ (Graphics3D rendering using threejs)
* `pymathics-natlang <https://github.com/Mathics3/pymathics-natlang>`_ (Natural Language Processing add-on)
* `pymathics-graph <https://github.com/Mathics3/pymathics-graph>`_ (Graph add-on based on `NetworkX <https://networkx.org/>`_.

It is likely that in the future more components will be added, so stay tuned...

.. |Packaging status| image:: https://repology.org/badge/vertical-allrepos/Mathics-omnibus.svg
			    :target: https://repology.org/project/Mathics-omnibus/versions
.. |Latest Version| image:: https://badge.fury.io/py/Mathics-omnibus.svg
		 :target: https://badge.fury.io/py/Mathics-omnibus
.. |Pypi Installs| image:: https://pepy.tech/badge/Mathics-omnibus
.. |Supported Python Versions| image:: https://img.shields.io/pypi/pyversions/Mathics-omnibus.svg


Docker-specific items
---------------------

By default, we use a SQLite database that has examples that you can
load and use. This data comes from
`mathics-omnibus/django-db/mathics.sqlite <https://github.com/Mathics3/mathics-omnibus/tree/master/docker/django-db>`_.

Since this is tied to the docker image, any changes made won't survice
across restarting the docker image.

If you would like to save your own you can set the environment
variable ``MATHICS_DJANGO_DB_PATH``. Here is an example:


.. code:: bash

   $ MATHICS_DJANGO_DB_PATH=/usr/src/app/data/mathics-django/mathics.sqlite ../mathics-omnibus/script/dmathicsserver
   MATHICS_DJANGO_DB_PATH=/usr/src/app/data/mathics-django/mathics.sqlite ../mathics-omnibus/script/dmathicsserver^J-(../mathics-omnibus/script/dmathicsserver:5):  -[2,0, 0]
   DOCKER=docker
   -(../mathics-omnibus/script/dmathicsserver:6):  -[2,0, 0]
   MATHICS_DJANGO_DB=mathics.sqlite
   -(../mathics-omnibus/script/dmathicsserver:7):  -[2,0, 0]
   MATHICS_DJANGO_DB_PATH=/usr/src/app/data/mathics-django/mathics.sqlite
   -(../mathics-omnibus/script/dmathicsserver:9):  -[2,0, 0]
   docker run -it --name mathics-web --rm --env=DISPLAY --env MATHICS_DJANGO_DB_PATH=/usr/src/app/data/mathics-django/mathics.sqlite --workdir=/app --volume=/src/external-vcs/github/Mathics3/mathics-django:/app --volume=/tmp/.X11-unix:/tmp/.X11-unix:rw -p 8000:8000 -v /tmp:/usr/src/app/data mathicsorg/mathics --mode ui

   ~~~~ app/data has been mounted to /usr/src/app/data ~~~~
   ~~~~ SQLite data (worksheets, user info) will be stored in /usr/src/app/data/mathics django/mathics.sqlite ~~~~
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    warning: database file /usr/src/app/data/mathics-django/mathics.sqlite not found

    Migrating database /usr/src/app/data/mathics-django/mathics.sqlite
    Operations to perform:
      Apply all migrations: auth, contenttypes, sessions, sites, web
    Running migrations:

In the above when it says ``mathics.sqlite not found`` an empty one is
created. The real location of it outside of the container is in
``/tmp/mathics-django/mathics.sqlite``.
