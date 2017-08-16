# snap-plugin-collector-jolokia

### Assumptions

In our case we have one Jolokia per app/pod (in contrast to having one Jolokia working with many JMX endpoints) so in initial attempt we were able to make some simplifications.

Our base idea for plugin is:

- the plugin accepts a list of working Jolokia endpoints in dedicated section of snap config
- on start, the plugin retrieves JMX metrics available on these endpoints; the metrics catalog is updated based on that
- task config can hold one (or more) Jolokia endpoints to read the metrics from and the list of metrics it's interested in

This approach has the following consequences:

- when the plugin starts, it requires that there is some Jolokia endpoint working
- metrics catalog is updated once (because of the plugin lifecycle) - if there are new endpoints used in tasks, metrics they can handle are restricted to this list
(which means even if the new endpoints introduce new metrics, new metrics cannot be served -- unless you change the global config to include the url and restart SNAP)

We still have a doubt what to do with response with non-base type.

### For packaging you would need:

- [acbuild](https://github.com/containers/build)
- [virtualenv](https://pypi.python.org/pypi/virtualenv)
- [pyenv](https://github.com/yyuu/pyenv)
- [pyenv virtualenv](https://github.com/yyuu/pyenv-virtualenv)

### Creating packages:

To create a package simply run `$ make pkg` in root directory.

In configuration doubts, please take a look into examples.

