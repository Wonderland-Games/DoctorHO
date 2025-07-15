from Foundation.Object.DemonObject import DemonObject


class ObjectMissClick(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

    def _onParams(self, params):
        super(ObjectMissClick, self)._onParams(params)
