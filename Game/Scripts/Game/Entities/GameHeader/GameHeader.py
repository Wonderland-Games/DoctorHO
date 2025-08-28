from MobileKit.Entities.Header.Header import Header as HeaderBase
from Game.Entities.HeaderComponents.Settings import Settings
from Game.Entities.HeaderComponents.Lives import Lives


class GameHeader(HeaderBase):
    def __init__(self):
        super(GameHeader, self).__init__()

    def _adjustSlotsPositions(self):
        viewport = Mengine.getGameViewport()
        header_size = self.object.getSize()

        if self.movie_content.hasSlot(Settings.slot_name):
            slot = self.movie_content.getMovieSlot(Settings.slot_name)
            slot.setWorldPosition(Mengine.vec2f(
                viewport.begin.x + header_size.x * 0.9,
                viewport.begin.y + header_size.y * 0.5
            ))

        if self.movie_content.hasSlot(Lives.slot_name):
            slot = self.movie_content.getMovieSlot(Lives.slot_name)
            slot.setWorldPosition(Mengine.vec2f(
                viewport.begin.x + header_size.x * 0.2,
                viewport.begin.y + header_size.y * 0.5
            ))

    def _setup(self):
        header_components = [Settings, Lives]
        for component in header_components:
            if self.movie_content.hasSlot(component.slot_name) is False:
                Trace.log("HeaderComponent", 0, "Not found slot {!r} in {!r}!".format(component.slot_name, self.__class__.__name__))
                continue

            component_instance = component()
            component_instance.onInitialize(self)
            self.content[component.slot_name] = component_instance
