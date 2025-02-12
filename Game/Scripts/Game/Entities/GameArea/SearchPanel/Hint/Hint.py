from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager


BUTTON_HINT = "Movie2Button_Hint"
MOVIE_HINT_EFFECT = "Movie2_HintEffect"
LAYER_HINT_EFFECT_CUTOUT = "Hint_Effect_Cutout_Cirlce_16.png"


class Hint(Initializer):
    def __init__(self):
        super(Hint, self).__init__()
        self._root = None
        self.game = None
        self.button = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        self.game = game

        self._createRoot()
        self._attachButton()

    def _onFinalize(self):
        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.game = None
        self.button = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self._root = Mengine.createNode("Interender")
        self._root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def getRoot(self):
        return self._root

    # - Button ---------------------------------------------------------------------------------------------------------

    def _attachButton(self):
        self.button = self.game.object.getObject(BUTTON_HINT)
        button_node = self.button.getEntityNode()
        self._root.addChild(button_node)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def clickHint(self, source):
        game_group = self.game.object.getGroupName()
        hint_effect = GroupManager.getObject(game_group, MOVIE_HINT_EFFECT)

        item_index = Mengine.range_rand(0, len(self.game.search_level.items))
        print(item_index)
        scene_item = self.game.search_level.items[item_index]
        print(scene_item.getName())
        scene_item_node = scene_item.getEntityNode()
        scene_item_node_transformation = scene_item_node.getTransformation()
        print(scene_item_node_transformation)

        hint_point = scene_item.calcWorldHintPoint()

        temp_hint_node = Mengine.createNode("Interender")
        temp_hint_node.setName("TempHintNode")

        self.game.addChild(temp_hint_node)
        temp_hint_node.setWorldPosition(hint_point)

        scene_item_node_transformation = temp_hint_node.getTransformation()

        hint_effect_movie = hint_effect.getMovie()

        source.addFunction(self.game.search_panel.hint.button.setBlock, True)

        source.addPrint("CLICKED HINT")

        source.addFunction(hint_effect.setEnable, True)
        source.addFunction(hint_effect_movie.setExtraTransformation, LAYER_HINT_EFFECT_CUTOUT, scene_item_node_transformation, True)
        source.addDelay(3000.0)
        source.addFunction(hint_effect_movie.removeExtraTransformation, LAYER_HINT_EFFECT_CUTOUT)
        source.addFunction(hint_effect.setEnable, False)

        source.addTask("TaskNodeRemoveFromParent", Node=temp_hint_node)
        source.addTask("TaskNodeDestroy", Node=temp_hint_node)

        source.addFunction(self.game.search_panel.hint.button.setBlock, False)
