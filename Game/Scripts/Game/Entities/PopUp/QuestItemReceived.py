from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from Game.Managers.GameManager import GameManager


SLOT_ITEM = "Item"


class QuestItemReceived(PopUpContent):
    content_id = "QuestItemReceived"

    def __init__(self):
        super(QuestItemReceived, self).__init__()

        self.item_sprite = None

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self, **content_args):
        super(QuestItemReceived, self)._onInitializeContent()

        self._setupItem(content_args["LevelName"], content_args["ItemName"])

    def _onFinalizeContent(self):
        super(QuestItemReceived, self)._onFinalizeContent()

        if self.item_sprite is not None:
            Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _generateItemSprite(self, item):
        item_entity = item.getEntity()
        item_sprite = item_entity.generatePure()
        item_sprite.enable()
        return item_sprite

    def _setupItem(self, level_name, item_name):
        level_item = GameManager.getLevelItem(level_name, item_name)
        if level_item is None:
            return

        self.item_sprite = self._generateItemSprite(level_item)

        slot = self.content.getMovieSlot(SLOT_ITEM)
        slot.addChild(self.item_sprite)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center.x, -item_sprite_center.y))
