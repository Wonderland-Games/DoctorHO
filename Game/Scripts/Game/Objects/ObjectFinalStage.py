from Foundation.Object.DemonObject import DemonObject


class ObjectFinalStage(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

    def _onParams(self, params):
        super(ObjectFinalStage, self)._onParams(params)
