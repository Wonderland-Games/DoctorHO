from MobileKit.Objects.ObjectHeader import ObjectHeader as ObjectHeaderBase


MOVIE_CONTENT = "Movie2_Content"


class ObjectGameHeader(ObjectHeaderBase):
    def getHeight(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "GameHeader entity is not active!")
            return 0.0

        content = self.getObject(MOVIE_CONTENT)
        bounding_box = content.getCompositionBounds()
        height = Utils.getBoundingBoxHeight(bounding_box)

        return height
