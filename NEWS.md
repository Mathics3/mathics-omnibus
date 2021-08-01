4.0.0
-----

# PyPI

Revised for Mathics 4.0.0. See the respective changes in Mathics3, Mathics-Django, and mathicsscript for changes there.

# Docker


* we now use `llvm12` and a more recent `gv`
* there is an `--upgrade` command added to all docker scripts to retrieve/updagte to the latest version
* More environment variables can be passed through.
* You can set environment variable `APP_DATADIR` to a directory outside Django to have data persist there. You may want to use this with `MATHIC_DJANGO_PATH` below...
* In `dmathicsscript`, if you set `MATHICS_DJANGO_DB_PATH` and that file doesn't exist, the system database will be copied to that location. This gives a way for persisting sessions outside of docker.

There is be interaction between `MATHICS_DJANGO_DB_PATH` and `APP_DATADIR` to get the database to persist.

As a simple example, run:

```
  $ MATHICS_DJANGO_DB_PATH=/usr/src/app/data/foo.sqlite dmathicsserver
```

Above, since by default `APP_DATADIR` maps `/usr/src/app/data` to `/tmp`, on the host filesystem in `/tmp/mathics-django.sqlite` workspace sessions can be saved.

3.1.0
-----

This version builds the PDF and stores that in the docker container. As a result two new
command and front-end shell scripts were added:

* `dmathicsdoc` will run _evince_ over the Mathics book that was built when the container was built.
* `dmathicsdoccopy` will copy the Mathics book that was built when the container was built.

The script for going into `mathicsscript` has been enhanced to try to detect the terminal background.

Set environment variable `COLORFGBG` to force what kind of background you have Use value `15;0` for dark backgrounds and `0;15` for light backgrounds.

Two new workspaces taken from "Implementing Discrete Mathematics" have been added to Mathics Django:

* C 3.1 Datastructures for Graphs
* C 3.2 Classifying Simple Graphs

Section 14: Coordinates and Graphics 3D has been revised now that the efficiency of threejs rendering has been improved. We can now easily compute 10x10 points in a box.

3.0.0
-----

Track changes to Mathics core Django, mathicsscript, and pymathics-graph.
Numerous docker config changes.


2.2.0
-----

Tracks Mathics 2.2.0 core release and related packages.

1.0.0
-----

First public release.

Pulls in

* Mathics3,
* mathicsscript, and
* mathics-django.

And pymathics modules:

* pymathics-natlang,
* pymathics-graph,
