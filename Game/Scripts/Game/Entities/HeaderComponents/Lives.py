from MobileKit.HeaderComponent import HeaderComponent
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.Managers.IconManager import IconManager


PROTOTYPE_BG = "HeaderLivesBackground"
SLOT_LIFE = "Life_{}"


class Lives(HeaderComponent):
    slot_name = "lives"

    def __init__(self):
        super(Lives, self).__init__()
        self._root = None
        self.background = None
        self.lives = []

    def _onPreparation(self):
        super(Lives, self)._onPreparation()

        if self.header.movie_content.hasMovieSlot(self.slot_name) is False:
            Trace.log("HeaderComponent", 0, "Not found slot {!r} in Header!".format(self.slot_name))
            return

        self._setupRoot()
        self._setupBackground()
        self._setupLives()

    def _onActivate(self):
        super(Lives, self)._onActivate()

        self.addObserver(Notificator.onLevelLivesDecrease, self._onLevelLivesDecrease)

    def _onFinalize(self):
        super(Lives, self)._onFinalize()

        for life in self.lives:
            if life is not None:
                life.onDestroy()
        self.lives = []

        if self.background is not None:
            self.background.onDestroy()
            self.background = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _setupRoot(self):
        self._root = Mengine.createNode("Interender")
        self._root.setName(self.__class__.__name__)

        slot_lives = self.header.movie_content.getMovieSlot(self.slot_name)
        slot_lives.addChild(self._root)

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def setLocalPosition(self, pos):
        self._root.setLocalPosition(pos)

    # - Background -----------------------------------------------------------------------------------------------------

    def _setupBackground(self):
        self.background = PrototypeManager.generateObjectUniqueOnNode(self._root, PROTOTYPE_BG, PROTOTYPE_BG)
        self.background.setEnable(True)

    def _getBackgroundSize(self):
        background_bounds = self.background.getCompositionBounds()
        background_size = Utils.getBoundingBoxSize(background_bounds)
        return background_size

    # - Lives ----------------------------------------------------------------------------------------------------------

    def _setupLives(self):
        hearts_count = 3
        for i in range(hearts_count):
            life = Life()
            life.onInitialize()

            life_slot = self.background.getMovieSlot(SLOT_LIFE.format(i+1))
            life_node = life.getRoot()
            life_slot.addChild(life_node)

            self.lives.append(life)

    def _onLevelLivesDecrease(self):
        if len(self.lives) is 0:
            return False

        full_lives = []
        for life in self.lives:
            life_state = life.getState()
            if life_state is True:
                full_lives.append(life)

        current_life = full_lives[-1]
        current_life.setState(False)

        full_lives_count = len(full_lives) - 1

        Notification.notify(Notificator.onLevelLivesChanged, full_lives_count)

        return False


ICON_LIVE = "Heart"


class Life(object):
    STATE_FULL = True
    STATE_DEAD = False

    def __init__(self):
        self._state = None
        self._root = None
        self._icon = None

    def onInitialize(self):
        self._state = self.STATE_FULL
        self._setupRoot()
        self._setupIcon()

    def onDestroy(self):
        if self._icon is not None:
            self._icon.onDestroy()
            self._icon = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self._state = None

    # - State ----------------------------------------------------------------------------------------------------------

    def setState(self, state):
        self._state = state
        self._updateIconState()

    def getState(self):
        return self._state

    # - Root -----------------------------------------------------------------------------------------------------------

    def _setupRoot(self):
        self._root = Mengine.createNode("Interender")
        self._root.setName(self.__class__.__name__)

    def getRoot(self):
        return self._root

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def setLocalPosition(self, pos):
        self._root.setLocalPosition(pos)

    # - Icon -----------------------------------------------------------------------------------------------------------

    def _setupIcon(self):
        self._icon = IconManager.generateIconOnNode(self._root, ICON_LIVE)
        self._icon.setEnable(True)

    def getSize(self):
        icon_bounds = self._icon.getCompositionBounds()
        icon_size = Utils.getBoundingBoxSize(icon_bounds)
        return icon_size

    def _updateIconState(self):
        if self._state is True:
            self._icon.setRGB((1.0, 1.0, 1.0))
            self._icon.setAlpha(1.0)
        else:
            self._icon.setRGB((0.0, 0.0, 0.0))
            self._icon.setAlpha(0.25)
