from Foundation.Object.DemonObject import DemonObject


class ObjectGameArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "LevelId", None)
        Type.addParam(Type, "FoundItems", None)
        Type.addParam(Type, "HintCount", None)

    def _onParams(self, params):
        super(ObjectGameArea, self)._onParams(params)
        self.initParam("LevelId", params, None)
        self.initParam("FoundItems", params, [])
        self.initParam("HintCount", params, 3)
