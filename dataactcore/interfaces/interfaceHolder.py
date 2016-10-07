from dataactcore.models.baseInterface import BaseInterface
from dataactbroker.handlers.errorHandler import ErrorHandler
from dataactbroker.handlers.jobHandler import JobHandler
from dataactbroker.handlers.userHandler import UserHandler
from dataactbroker.interfaces.validationBrokerInterface import ValidationBrokerInterface

class InterfaceHolder:
    """ This class holds an interface to each database as a static variable, to allow reuse of connections throughout the project """
    def __init__(self, forceOverwrite = False):
        """ Create the interfaces """
        if BaseInterface.interfaces is None or forceOverwrite:
            self.jobDb = JobHandler()
            self.errorDb = ErrorHandler()
            self.userDb = UserHandler()
            self.validationDb = ValidationBrokerInterface()
            self.stagingDb = self.validationDb
            BaseInterface.interfaces = self
        else:
            self.jobDb = BaseInterface.interfaces.jobDb
            self.errorDb = BaseInterface.interfaces.errorDb
            self.userDb = BaseInterface.interfaces.userDb
            self.validationDb = BaseInterface.interfaces.validationDb
            self.stagingDb = self.validationDb

    def close(self):
        """ Close all open connections """
        if self.jobDb is not None:
            self.jobDb.close()