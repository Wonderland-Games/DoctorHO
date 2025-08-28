from MobileKit.Objects.ObjectHeader import ObjectHeader as ObjectHeaderBase
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


class ObjectGameHeader(ObjectHeaderBase):
    def getSize(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "Header entity is not active!")
            return Mengine.vec2f(0.0, 0.0)

        content = self.getObject("Movie2_Content")
        bbox = content.getCompositionBounds()

        width = AdjustableScreenUtils.getGameWidth()
        height = bbox.maximum.y - bbox.minimum.y
        return Mengine.vec2f(width, height)

    def getHeight(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "Header entity is not active!")
            return 0.0
        header_size = self.getSize()
        return header_size.y
