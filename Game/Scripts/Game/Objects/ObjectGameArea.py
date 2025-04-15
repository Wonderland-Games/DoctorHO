from Foundation.Object.DemonObject import DemonObject


class ObjectGameArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "ChapterId", None)
        Type.addParam(Type, "LevelId", None)
        Type.addParam(Type, "QuestIndex", None)
        Type.addParam(Type, "FoundItems", None)
        Type.addParam(Type, "HintCount", None)

    def _onParams(self, params):
        super(ObjectGameArea, self)._onParams(params)
        self.initParam("ChapterId", params, None)
        self.initParam("LevelId", params, None)
        self.initParam("QuestIndex", params, None)
        self.initParam("FoundItems", params, [])
        self.initParam("HintCount", params, 3)
