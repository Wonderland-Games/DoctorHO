from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea


class SearchLevel(Initializer):
    def __init__(self):
        super(SearchLevel, self).__init__()
        self.root = None
        self.game = None
        self.level_name = None
        self.items = None

    def _onInitialize(self, game, level_name):
        self.game = game
        self.level_name = level_name

        self._createRoot()
        self._attachScene()
        self._fillItems()

        return True

    def _onFinalize(self):
        self.game = None
        self.level_name = None
        self.items = None

        if self.root is not None:
            Mengine.destroyNode(self.root)
            self.root = None

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + self.level_name)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def _attachScene(self):
        level_group = GroupManager.getGroup(self.level_name)
        level_group_scene = level_group.getScene()
        scene_node = level_group_scene.getParent()

        self.root.addChild(scene_node)

        scene_size = self.getSize()
        scene_pos = Mengine.vec2f(-scene_size.x / 2, -scene_size.y / 2)
        scene_node.setLocalPosition(scene_pos)
        level_group_scene.enable()

    def _fillItems(self):
        level_group = GroupManager.getGroup(self.level_name)
        level_group_objects = level_group.getObjects()

        self.items = [item for item in level_group_objects if item.getEntityType() is "Item"]

    def getSize(self):
        level_group = GroupManager.getGroup(self.level_name)
        level_group_scene = level_group.getScene()
        level_group_scene_layer = level_group_scene.getParent()
        level_group_scene_layer_size = level_group_scene_layer.getSize()
        return level_group_scene_layer_size
