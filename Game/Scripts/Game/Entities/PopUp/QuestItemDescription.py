from UIKit.Entities.PopUp.PopUpContent import PopUpContent
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
        self._setupItemName()
        self._setupItemDescriptionFull()

        self._adjustSlotsPositions()

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

        item_size = self.item_sprite.getSurfaceSize()
        scale_perc_x = ITEM_BOX_SIZE / item_size.x
        scale_perc_y = ITEM_BOX_SIZE / item_size.y
        scale_perc = min(scale_perc_x, scale_perc_y)
        self.item_sprite.setScale((scale_perc, scale_perc, 1.0))

        slot = self.content.getMovieSlot(SLOT_ITEM_SPRITE)
        slot.addChild(self.item_sprite)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center.x * scale_perc, -item_sprite_center.y * scale_perc))

    def _setupItemName(self):
        self.item_name = Mengine.createNode("TextField")
        self.item_name.setName(self.item_codename + "_" + TEXT_ITEM_NAME_ANNEX)

        self.item_name.setVerticalCenterAlign()
        self.item_name.setHorizontalCenterAlign()

        self.item_name.setTextId(TEXT_ITEM_NAME)
        item_name_text_id = TEXT_ITEM_NAME_TEMPLATE.format(self.item_codename, TEXT_ITEM_NAME_ANNEX)
        item_name_text = Mengine.getTextFromId(item_name_text_id)
        self.item_name.setTextFormatArgs(item_name_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_NAME)
        slot.addChild(self.item_name)

        self.item_name.enable()

    def _setupItemDescriptionFull(self):
        self.item_description_full = Mengine.createNode("TextField")
        self.item_description_full.setName(self.item_codename + "_" + TEXT_ITEM_DESCRIPTION_FULL_ANNEX)

        self.item_description_full.setVerticalCenterAlign()
        self.item_description_full.setHorizontalCenterAlign()

        self.item_description_full.setTextId(TEXT_ITEM_DESCRIPTION_FULL)
        item_description_full_text_id = TEXT_ITEM_DESCRIPTION_FULL_TEMPLATE.format(self.item_codename, TEXT_ITEM_DESCRIPTION_FULL_ANNEX)
        item_description_full_text = Mengine.getTextFromId(item_description_full_text_id)
        self.item_description_full.setTextFormatArgs(item_description_full_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_DESCRIPTION)
        slot.addChild(self.item_description_full)

        self.item_description_full.enable()

    def _adjustSlotsPositions(self):
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
