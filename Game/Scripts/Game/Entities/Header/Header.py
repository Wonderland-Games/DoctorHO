from MobileKit.Entities.Header.Header import Header as HeaderBase
from Game.Entities.HeaderComponents.Settings import Settings
from Foundation.SceneManager import SceneManager


SETTINGS_BLACKLIST = [
    "Cutscene",
]


class Header(HeaderBase):

    def __init__(self):
        super(Header, self).__init__()

    def _adjustSlotsPositions(self):
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        header_size = self.object.getSize()
        space_before_header = (game_width - header_size.x) / 2

        if self.movie_content.hasSlot(Settings.slot_name):
            slot = self.movie_content.getMovieSlot(Settings.slot_name)
            slot.setWorldPosition(Mengine.vec2f(
                viewport.begin.x + space_before_header + header_size.x * 0.9,
                viewport.begin.y + header_size.y * 0.5
            ))

    def _setup(self):
        current_scene = SceneManager.getCurrentSceneName()
        header_components = [Settings]
        for component in header_components:
            if self.movie_content.hasSlot(component.slot_name) is False:
                Trace.log("HeaderComponent", 0, "Not found slot {!r} in {!r}!".format(component.slot_name, self.__class__.__name__))
                continue

            if current_scene in SETTINGS_BLACKLIST:
                continue

            component_instance = component()
            component_instance.onInitialize(self)
            self.content[component.slot_name] = component_instance
