from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from UIKit.LayoutWrapper.LayoutSpriteWrapper import LayoutSpriteWrapper
from Game.Managers.GameManager import GameManager


SLOT_ITEM = "Item"
SLOT_BUTTON = "Button"

ITEM_BOX_SIZE = 500.0


class QuestItemReceived(PopUpContent):
    content_id = "QuestItemReceived"

    def __init__(self):
        super(QuestItemReceived, self).__init__()

        self.item_object = None
        self.item_sprite = None
        self.button = None
        self.isHoldingItem = False

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self, **content_args):
        super(QuestItemReceived, self)._onInitializeContent()

        self._setupItem(content_args["ItemName"])
        self._setupButton()
        self._setupLayoutBox()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(QuestItemReceived, self)._onFinalizeContent()

        if None not in [self.item_sprite, self.item_object]:
            if self.isHoldingItem is True:
                self.item_object.onDestroy()
            self.item_object = None
            self.item_sprite = None

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupItem(self, item_name):
        self.item_object = GameManager.generateQuestItem(item_name)
        self.item_sprite = self.item_object.entity.getSprite()
        self.item_sprite.enable()

        self.isHoldingItem = True

        item_size = self.item_sprite.getSurfaceSize()
        scale_perc_x = ITEM_BOX_SIZE / item_size.x
        scale_perc_y = ITEM_BOX_SIZE / item_size.y
        scale_perc = min(scale_perc_x, scale_perc_y)
        self.item_sprite.setScale((scale_perc, scale_perc, 1.0))

        slot = self.content.getMovieSlot(SLOT_ITEM)
        slot.addChild(self.item_sprite)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.item_sprite.setLocalPosition((-item_sprite_center.x * scale_perc, -item_sprite_center.y * scale_perc))

    def _setupButton(self):
        self.button = self._generateContainter(SLOT_BUTTON)
        if self.button is None:
            return

        self._attachObjectToSlot(self.button, SLOT_BUTTON)

    def _setupLayoutBox(self):
        item_sprite_wrapper = LayoutSpriteWrapper(self.item_sprite)

        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            vertical.addPadding(1)
            vertical.addFixedObject(item_sprite_wrapper)
            vertical.addPadding(1)
            vertical.addFixedObject(self.button)
            vertical.addPadding(1)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        if self.button is not None:
            with self._createTaskChain(SLOT_BUTTON) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.button.movie)
                tc.addScope(self._scopeButton)

    def _scopeButton(self, source):
        self.isHoldingItem = False

        source.addNotify(Notificator.onPopUpQuestItemReceived)
