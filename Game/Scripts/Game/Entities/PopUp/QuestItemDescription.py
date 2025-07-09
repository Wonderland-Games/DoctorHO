from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from Foundation.GroupManager import GroupManager


SLOT_ITEM_SPRITE = "ItemSprite"

SLOT_ITEM_NAME = "ItemName"
SLOT_ITEM_DESCRIPTION = "ItemDescriptionFull"

TEXT_ITEM_NAME_ANNEX = "Name"
TEXT_ITEM_DESCRIPTION_FULL_ANNEX = "DescriptionFull"

TEXT_ITEM_NAME = "ID_QuestItem_{}".format(TEXT_ITEM_NAME_ANNEX)
TEXT_ITEM_DESCRIPTION_FULL = "ID_QuestItem_{}".format(TEXT_ITEM_DESCRIPTION_FULL_ANNEX)

TEXT_ITEM_NAME_TEMPLATE = "ID_QuestItem_{}_{}"
TEXT_ITEM_DESCRIPTION_FULL_TEMPLATE = "ID_QuestItem_{}_{}"

ITEM_BOX_SIZE = 500.0
TEXT_ITEM_DESCRIPTION_LENGTH_PERCENT = 0.9

QUEST_ITEM_STORE_GROUP = "QuestItemStore"
QUEST_ITEM_NAME = "Item_{}_{}"


class QuestItemDescription(PopUpContent):
    content_id = "QuestItemDescription"

    def __init__(self):
        super(QuestItemDescription, self).__init__()

        self.item_codename = None
        self.item_sprite = None
        self.item_name = None
        self.item_description_full = None

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self, **content_args):
        super(QuestItemDescription, self)._onInitializeContent()

        chapter_id = content_args["ChapterId"]
        item_name = content_args["ItemName"]
        convert_to_store_item_name = content_args.get("ConvertToStoreItemName", True)

        if convert_to_store_item_name is True:
            item_name_raw = item_name.replace("Item_", "")
            self.item_codename = QUEST_ITEM_NAME.format(chapter_id, item_name_raw)
        else:
            self.item_codename = item_name

        self._setupItemSprite()
        # self._setupItemName()
        self._setupPopUpTitle()
        self._setupItemDescriptionFull()

        # self._adjustSlotsPositions()
        self._setupLayoutBox()

    def _onFinalizeContent(self):
        super(QuestItemDescription, self)._onFinalizeContent()

        if self.item_description_full is not None:
            Mengine.destroyNode(self.item_description_full)
            self.item_description_full = None

        if self.item_name is not None:
            Mengine.destroyNode(self.item_name)
            self.item_name = None

        if self.item_sprite is not None:
            Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

        self.item_codename = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupItemSprite(self):
        item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
        item_object = item_store_group.getObject(self.item_codename)
        item_entity = item_object.getEntity()
        self.item_sprite = item_entity.generatePure()
        self.item_sprite.enable()

        sprite_scale = self._getSpriteScale()
        self.item_sprite.setScale(sprite_scale)

        slot = self.content.getMovieSlot(SLOT_ITEM_SPRITE)
        slot.addChild(self.item_sprite)

        sprite_size = self._getSpriteSize()
        popup_content_size = self.pop_up_base.getContentSize()
        # changing pos not working on slot somehow, so lets try change item sprite pos instead
        self.item_sprite.setLocalPosition(Mengine.vec2f(
            -sprite_size.x / 2,
            -popup_content_size.y / 2
        ))

    def _getSpriteScale(self):
        item_size = self.item_sprite.getSurfaceSize()
        scale_perc_x = ITEM_BOX_SIZE / item_size.x
        scale_perc_y = ITEM_BOX_SIZE / item_size.y
        scale_perc = min(scale_perc_x, scale_perc_y)
        sprite_scale = Mengine.vec3f(scale_perc, scale_perc, 1.0)
        return sprite_scale

    def _getSpriteSize(self):
        item_sprite_center = self.item_sprite.getLocalImageCenter()
        sprite_scale = self._getSpriteScale()
        sprite_size = Mengine.vec2f(item_sprite_center.x * 2 * sprite_scale.x, item_sprite_center.y * 2 * sprite_scale.y)
        return sprite_size

    def _setupItemName(self):
        self.item_name = Mengine.createNode("TextField")
        self.item_name.setName(self.item_codename + "_" + TEXT_ITEM_NAME_ANNEX)

        self.item_name.setVerticalBottomAlign()
        self.item_name.setHorizontalCenterAlign()

        self.item_name.setTextId(TEXT_ITEM_NAME)
        item_name_text_id = TEXT_ITEM_NAME_TEMPLATE.format(self.item_codename, TEXT_ITEM_NAME_ANNEX)
        item_name_text = Mengine.getTextFromId(item_name_text_id)
        self.item_name.setTextFormatArgs(item_name_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_NAME)
        slot.addChild(self.item_name)

        popup_content_size = self.pop_up_base.getContentSize()
        sprite_size = self._getSpriteSize()
        slot.setLocalPosition(Mengine.vec2f(0, -popup_content_size.y / 2 + sprite_size.y))

        self.item_name.enable()

    def _setupPopUpTitle(self):
        item_name_text_id = TEXT_ITEM_NAME_TEMPLATE.format(self.item_codename, TEXT_ITEM_NAME_ANNEX)
        self.title_text_id = item_name_text_id

    def _setupItemDescriptionFull(self):
        self.item_description_full = Mengine.createNode("TextField")
        self.item_description_full.setName(self.item_codename + "_" + TEXT_ITEM_DESCRIPTION_FULL_ANNEX)

        # self.item_description_full.setVerticalBottomAlign()    # deprecated method
        self.item_description_full.setVerticalCenterAlign()
        self.item_description_full.setHorizontalCenterAlign()

        self.item_description_full.setJustify(True)

        self.item_description_full.setTextId(TEXT_ITEM_DESCRIPTION_FULL)
        item_description_full_text_id = TEXT_ITEM_DESCRIPTION_FULL_TEMPLATE.format(self.item_codename, TEXT_ITEM_DESCRIPTION_FULL_ANNEX)
        item_description_full_text = Mengine.getTextFromId(item_description_full_text_id)
        self.item_description_full.setTextFormatArgs(item_description_full_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_DESCRIPTION)
        slot.addChild(self.item_description_full)

        popup_content_size = self.pop_up_base.getContentSize()
        # sprite_size = self._getSpriteSize()
        # slot.setLocalPosition(Mengine.vec2f(0, -popup_content_size.y / 2 + sprite_size.y))    # deprecated method

        self.item_description_full.setMaxLength(popup_content_size.x)

        self.item_description_full.enable()

    def _adjustSlotsPositions(self):    # deprecated method
        content_size = self.pop_up_base.getContentSize()
        item_size_raw = self.item_sprite.getSurfaceSize()
        item_scale = self.item_sprite.getScale()
        item_size = Mengine.vec2f(item_size_raw.x * item_scale.x, item_size_raw.y * item_scale.y)
        available_size_y = content_size.y - item_size.y  # - button_size.y

        slots_data = {
            SLOT_ITEM_SPRITE: item_size.y / 2,
            # SLOT_BUTTON: button_size.y / 2,
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

        class TextWrapper:
            def __init__(self, text):
                self.text = text

            def getTextSize(self):
                # text_size = self.text.calcTotalTextSize()
                text_size = self.text.getTextSize()
                return (text_size.x, text_size.y)

            def getLayoutSize(self):
                return self.getTextSize()

            def setLayoutOffset(self, layout_box, layout_offset, layout_size):
                layout_box_width, layout_box_height = layout_box.getSize()
                self.text.setLocalPosition((
                    layout_offset[0] + layout_size[0] / 2 - layout_box_width / 2,
                    layout_offset[1] + layout_size[1] / 2 - layout_box_height / 2
                ))

        item_description_full_wrapper = TextWrapper(self.item_description_full)

        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            vertical.addPadding(1)
            vertical.addFixedObject(item_sprite_wrapper)
            vertical.addPadding(1)
            vertical.addFixedObject(item_description_full_wrapper)
            vertical.addPadding(1)
