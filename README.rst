============
KOOK PROJECT
============

Kook is a robust recipe inventory storing and sharing SaaS. It is built
on Pyramid framework and is open source only while in development.

Key features:
    * multiple versions of a recipe, sorted by user rating
    * ingredient measures converting system
    * recipe cooking time is calculated through cooking steps timing
    * user reputation (inspired by Stackoverflow)
    * recipes have tags
    * mobile version to take *kook* with the cook to kitchen

Install and run
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/populate_kook development.ini

- $venv/bin/pserve development.ini

