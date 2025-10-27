from Foundation.Object.DemonObject import DemonObject


class ObjectGameArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareParam("ChapterId", None)
        Type.declareParam("LevelId", None)
        Type.declareParam("QuestIndex", None)
        Type.declareParam("FoundItems", None)
        Type.declareParam("HintCount", None)

    def _onParams(self, params):
        super(ObjectGameArea, self)._onParams(params)
        self.initParam("ChapterId", params, None)
        self.initParam("LevelId", params, None)
        self.initParam("QuestIndex", params, None)
        self.initParam("FoundItems", params, [])
        self.initParam("HintCount", params, 3)
