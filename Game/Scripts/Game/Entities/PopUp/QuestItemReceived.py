from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from Foundation.GroupManager import GroupManager


SLOT_ITEM = "Item"
SLOT_BUTTON = "Button"

ITEM_BOX_SIZE = 500.0

QUEST_ITEM_STORE_GROUP = "QuestItemStore"
QUEST_ITEM_NAME = "Item_{}_{}"


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

        self._setupItem(content_args["ChapterId"], content_args["ItemName"])
        self._setupButton()

        # self._adjustSlotsPositions()
        self._setupLayoutBox()

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

    def _setupItem(self, chapter_id, item_name):
        item_name_raw = item_name.replace("Item_", "")
        item_name_store = QUEST_ITEM_NAME.format(chapter_id, item_name_raw)

        item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
        item_object = item_store_group.getObject(item_name_store)
        item_entity = item_object.getEntity()
        self.item_sprite = item_entity.generatePure()
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
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center.x * scale_perc, -item_sprite_center.y * scale_perc))

    def _setupButton(self):
        self.button = self._generateContainter(SLOT_BUTTON)
        if self.button is None:
            return

        self._attachObjectToSlot(self.button, SLOT_BUTTON)

    def _adjustSlotsPositions(self):     # deprecated method
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

    def _setupLayoutBox(self):
        class SpriteWrapper:
            def __init__(self, sprite):
                self.sprite = sprite

            def getSpriteSize(self):
                sprite_size_unscaled = self.sprite.getSurfaceSize()
                sprite_scale = self.sprite.getScale()
                sprite_size = (sprite_size_unscaled.x * sprite_scale.x, sprite_size_unscaled.y * sprite_scale.y)
                return sprite_size

            def getLayoutSize(self):
                return self.getSpriteSize()

            def setLayoutOffset(self, layout_box, layout_offset, layout_size):
                layout_box_width, layout_box_height = layout_box.getSize()
                sprite_size = self.getSpriteSize()
                self.sprite.setLocalPosition((
                    layout_offset[0] + layout_size[0] / 2 - layout_box_width / 2 - sprite_size[0] / 2,
                    layout_offset[1] + layout_size[1] / 2 - layout_box_height / 2 - sprite_size[1] / 2
                ))

        item_sprite_wrapper = SpriteWrapper(self.item_sprite)

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
