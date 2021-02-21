`Mathics <https://mathics.org>`_ consists of a number of separable components so that those pieces that are desired can be used without the burden of dependencies of the other parts.

For example if you are interested in just running a command-line interface, you might not be interested in having Django and what that entails and vice versa.
If you are just interested in the computational library, there is no need for either the Web parts or the command-line library parts.

But what if you want both command-line interface, Web interface, all of the Pymathics libraries and whatever else there is to offer?

That's what this repository is about. Here we have a PyPI installable package that pull in the various components and offer commands

* ``mathicsscript`` to run the command-line interface
* ``mathicsserver`` to run the Django-Web server
* ``dmathicsscript`` and ``dmathicsserver`` which run the docker version of these.

This repository also contains the dockerfiile to create the `mathicsorg/mathics docker images <https://hub.docker.com/repository/docker/mathicsorg/mathics>`_.

That image is a combination of:

* `Mathics <https://github.com/mathics/Mathics>`_
* `mathicsscript <https://github.com/Mathics3/mathicsscript>`_
* `Mathics-Django <https://github.com/Mathics3/Mathics-Django>`_
* `pymathics-natlang <https://github.com/Mathics3/pymathics-natlang>`_
* `pymathics-graph <https://github.com/Mathics3/pymathics-graph>`_

It is likely that in the future more components will be added, so stay tuned...
