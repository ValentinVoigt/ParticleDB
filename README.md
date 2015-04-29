ParticleDB
==========

ParticleDB is a webinterface for managing your electronic parts.
 
Changing working directory
--------------------------

    cd <directory containing this file>

Configuration
-------------

    cp development.ini.default development.ini

Edit development.ini to your needs.

Getting Started
---------------

    $VENV/bin/python setup.py develop
    $VENV/bin/initialize_ParticleDB_db development.ini
    $VENV/bin/pserve development.ini
