from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from Foundation.GroupManager import GroupManager


SLOT_ITEM = "Item"
SLOT_BUTTON = "Button"

ITEM_BOX_SIZE = 500.0


class QuestItemReceived(PopUpContent):
    content_id = "QuestItemReceived"

    def __init__(self):
        super(QuestItemReceived, self).__init__()

        self.item_sprite = None
        self.button = None
        self.isHoldingItem = False

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self, **content_args):
        super(QuestItemReceived, self)._onInitializeContent()

        self._setupItem(content_args["GroupName"], content_args["ItemName"])
        self._setupButton()

        self._adjustSlotsPositions()
        self._runTaskChains()

    def _onFinalizeContent(self):
        super(QuestItemReceived, self)._onFinalizeContent()

        if self.item_sprite is not None:
            if self.isHoldingItem is True:
                Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _getItemFromGroup(self, group_name, item_name):
        group = GroupManager.getGroup(group_name)
        item = group.getObject(item_name)
        return item

    def _generateItemSprite(self, item):
        item_entity = item.getEntity()
        item_sprite = item_entity.generatePure()
        item_sprite.enable()
        return item_sprite

    def _setupItem(self, group_name, item_name):
        item = self._getItemFromGroup(group_name, item_name)
        self.item_sprite = self._generateItemSprite(item)
        self.isHoldingItem = True

        item_size = self.item_sprite.getSurfaceSize()
        scale_perc_x = ITEM_BOX_SIZE / item_size.x
        scale_perc_y = ITEM_BOX_SIZE / item_size.y
        scale_perc = min(scale_perc_x, scale_perc_y)
        self.item_sprite.setScale((scale_perc, scale_perc, 1.0))

        slot = self.content.getMovieSlot(SLOT_ITEM)
        slot.addChild(self.item_sprite)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center.x * scale_perc, -item_sprite_center.y * scale_perc))

    def _setupButton(self):
        self.button = self._generateContainter(SLOT_BUTTON)
        if self.button is None:
            return

        self._attachObjectToSlot(self.button, SLOT_BUTTON)

    def _adjustSlotsPositions(self):
        content_size = self.pop_up_base.getContentSize()
        item_size_raw = self.item_sprite.getSurfaceSize()
        item_scale = self.item_sprite.getScale()
        item_size = Mengine.vec2f(item_size_raw.x * item_scale.x, item_size_raw.y * item_scale.y)
        button_size = self.button.getSize()
        available_size_y = content_size.y - item_size.y - button_size.y

        slots_data = {
            SLOT_ITEM: item_size.y / 2,
            SLOT_BUTTON: button_size.y / 2,
        }
        offset_between_slots = available_size_y / (len(slots_data) + 1)
        current_pos_y = -content_size.y / 2

        for slot_name, obj_half_size in slots_data.items():
            slot = self.content.getMovieSlot(slot_name)

            current_pos_y += offset_between_slots
            current_pos_y += obj_half_size

            slot.setLocalPosition(Mengine.vec2f(0, current_pos_y))

            current_pos_y += obj_half_size

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        if self.button is not None:
            with self._createTaskChain(SLOT_BUTTON) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.button.movie)
                tc.addScope(self._scopeButton)

    def _scopeButton(self, source):
        self.isHoldingItem = False

        source.addNotify(Notificator.onPopUpHide)
