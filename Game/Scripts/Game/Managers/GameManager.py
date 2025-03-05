from Foundation.Manager import Manager


class GameManager(Manager):
    @classmethod
    def _onInitialize(cls, *args):
        print "INITIALIZING"

    @classmethod
    def _onLoad(cls, dict_save):
        print "LOADING SAVE"
