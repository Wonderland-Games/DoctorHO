from Foundation.Object.DemonObject import DemonObject


class ObjectGameArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "GameType", None)
        Type.addParam(Type, "LevelName", None)

    def _onParams(self, params):
        super(ObjectGameArea, self)._onParams(params)
        self.initParam("GameType", params, None)
        self.initParam("LevelName", params, None)
