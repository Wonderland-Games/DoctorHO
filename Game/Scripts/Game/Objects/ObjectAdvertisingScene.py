from Foundation.Object.DemonObject import DemonObject


class ObjectAdvertisingScene(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "NextScene")
        Type.addParam(Type, "AdPlacement")

    def _onParams(self, params):
        super(ObjectAdvertisingScene, self)._onParams(params)
        self.initParam("NextScene", params, None)
        self.initParam("AdPlacement", params, None)
