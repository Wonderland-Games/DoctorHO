from MobileKit.Entities.Header.Header import Header as HeaderBase
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from Game.Entities.HeaderComponents.Settings import Settings


class Header(HeaderBase):

    def __init__(self):
        super(Header, self).__init__()

    def _adjustSlotsPositions(self):
        header_width, _, header_height, _, viewport, _, _ = AdjustableScreenUtils.getMainSizesExt()

        if self.movie_content.hasSlot(Settings.slot_name):
            slot = self.movie_content.getMovieSlot(Settings.slot_name)
            slot.setWorldPosition(Mengine.vec2f(
                viewport.begin.x + header_width * 0.85,
                viewport.begin.y + header_height * 0.5
            ))

    def _setup(self):
        header_components = [Settings]
        for component in header_components:
            if self.movie_content.hasSlot(component.slot_name) is False:
                Trace.log("HeaderComponent", 0, "Not found slot {!r} in {!r}!".format(component.slot_name, self.__class__.__name__))
                continue

            component_instance = component()
            component_instance.onInitialize(self)
            self.content[component.slot_name] = component_instance
