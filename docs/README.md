# Sphinx Documentation
The documentation is built using sphinx.  The master toctree
document is index.rst.


### Generate Docs from Docstrings

    sphinx-apidoc -o docs/source/api pybeam

    cd docs/
    .\make.bat html


Docs will be created with index.html in build/