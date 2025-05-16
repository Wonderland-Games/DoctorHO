from Foundation.Object.DemonObject import DemonObject


class ObjectCutscene(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "CutsceneId")

    def _onParams(self, params):
        super(ObjectCutscene, self)._onParams(params)
        self.initParam("CutsceneId", params, None)
