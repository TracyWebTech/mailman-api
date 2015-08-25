
Tests!
======

To make it easier to run the tests we require `Docker` to be installed. NOTE: on Debian-like systems, 'docker' suits for a graphical dock-like widgets, you may want to install 'docker.io' instead.

To run the tests just run `make test` inside the `tests` folder. This will pull a docker image from docker.hub and run tests on it. In case you want a local image, just run `make image` and a local image will be created.
