# ClassRank

This repository contains a Python implementation of the algorithm ClassRank. ClassRank is a nowel technique handy for measuring the relevance of each class in an RDF grpah.

Prerequisites
-------------

- Python 2.7 (64-bit version if you want to compute huge datastes)
- All the libraries listed in the file requirements.txt

Execution
---------
At the moment we are no providing installing methods, just the original python scripts. If you are planning to integrte this code with some other project you may have to deal with issues related to paths. We will be providing soon nicier ways to interact with this library. 

Example code
------------

The easiest way to execute ClassRank is using the function 'generate_pagerank()' located in helpers.classrank:
.. code:: python
    import code
    import other code


Contributing
------------
Theoretically, ClassRank can be applied to any kind of sirected graph. This prototype is ready to compute a limited set of formats. However, it has been developed following a modular architecture that allow to easily add new formats by implementing some ad-hoc parsers or formatters.
