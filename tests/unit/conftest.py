from random import randint

import pytest

import dataactcore.config
from dataactcore.scripts.databaseSetup import (
    createDatabase, dropDatabase, runMigrations)
from dataactvalidator.interfaces.interfaceHolder import InterfaceHolder

@pytest.fixture(scope='session')
def database():
    """Sets up a clean database, yielding a relevant interface holder"""
    print("Setting up validator interface")
    rand_id = str(randint(1, 9999))

    config = dataactcore.config.CONFIG_DB
    config['db_name'] = 'unittest{}_data_broker'.format(rand_id)
    print("Validator db name: " + config["db_name"])
    dataactcore.config.CONFIG_DB = config

    createDatabase(config['db_name'])
    runMigrations()
    interface = InterfaceHolder()

    yield interface

    interface.close()
    dropDatabase(config['db_name'])

