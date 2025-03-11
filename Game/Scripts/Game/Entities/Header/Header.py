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
        settings = Settings()
        settings.onInitialize(self)
        self.content[Settings.slot_name] = settings
