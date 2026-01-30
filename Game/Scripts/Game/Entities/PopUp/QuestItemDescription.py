from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from UIKit.LayoutWrapper.LayoutSpriteWrapper import LayoutSpriteWrapper
from UIKit.LayoutWrapper.LayoutTextWrapper import LayoutTextWrapper
from Game.Managers.GameManager import GameManager


SLOT_ITEM_SPRITE = "ItemSprite"

SLOT_ITEM_NAME = "ItemName"
SLOT_ITEM_DESCRIPTION = "ItemDescriptionFull"

TEXT_ITEM_NAME_ANNEX = "Name"
TEXT_ITEM_DESCRIPTION_FULL_ANNEX = "DescriptionFull"

TEXT_ITEM_NAME = "ID_QuestItem_{}".format(TEXT_ITEM_NAME_ANNEX)
TEXT_ITEM_DESCRIPTION_FULL = "ID_QuestItem_{}".format(TEXT_ITEM_DESCRIPTION_FULL_ANNEX)

TEXT_ITEM_NAME_TEMPLATE = "ID_QuestItem_{}_{}_{}"
TEXT_ITEM_DESCRIPTION_FULL_TEMPLATE = "ID_QuestItem_{}_{}_{}"

ITEM_BOX_SIZE = 500.0
TEXT_ITEM_DESCRIPTION_LENGTH_PERCENT = 0.9


class QuestItemDescription(PopUpContent):
    content_id = "QuestItemDescription"

    def __init__(self):
        super(QuestItemDescription, self).__init__()

        self.item_name = None
        self.item_sprite = None
        self.text_name = None
        self.text_description_full = None

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self, **content_args):
        super(QuestItemDescription, self)._onInitializeContent()
        self.item_name = content_args["ItemName"]

        self._setupItemSprite()
        # self._setupItemName()
        self._setupPopUpTitle()
        self._setupItemDescriptionFull()
        self._setupLayoutBox()

    def _onFinalizeContent(self):
        super(QuestItemDescription, self)._onFinalizeContent()

        if self.text_description_full is not None:
            Mengine.destroyNode(self.text_description_full)
            self.text_description_full = None

        if self.text_name is not None:
            Mengine.destroyNode(self.text_name)
            self.text_name = None

        if self.item_sprite is not None:
            Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

        self.item_name = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupItemSprite(self):
        # Temporary generating object
        self.item_sprite = GameManager.generateQuestItemNode(self.item_name)

        sprite_scale = self._getSpriteScale()
        self.item_sprite.setScale(sprite_scale)

        slot = self.content.getMovieSlot(SLOT_ITEM_SPRITE)
        slot.addChild(self.item_sprite)

        sprite_size = self._getSpriteSize()
        popup_content_size = self.pop_up_base.getContentSize()
        # changing pos not working on slot somehow, so lets try change item sprite pos instead
        self.item_sprite.setLocalPosition((
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
        self.text_name = Mengine.createNode("TextField")
        self.text_name.setName(self.item_name + "_" + TEXT_ITEM_NAME_ANNEX)

        self.text_name.setVerticalBottomAlign()
        self.text_name.setHorizontalCenterAlign()

        self.text_name.setTextId(TEXT_ITEM_NAME)
        chapter_id = GameManager.getCurrentChapterId()
        item_name_text_id = TEXT_ITEM_NAME_TEMPLATE.format(chapter_id, self.item_name, TEXT_ITEM_NAME_ANNEX)
        item_name_text = Mengine.getTextFromId(item_name_text_id)
        self.text_name.setTextFormatArgs(item_name_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_NAME)
        slot.addChild(self.text_name)

        popup_content_size = self.pop_up_base.getContentSize()
        sprite_size = self._getSpriteSize()
        slot.setLocalPosition((0, -popup_content_size.y / 2 + sprite_size.y))

        self.text_name.enable()

    def _setupPopUpTitle(self):
        chapter_id = GameManager.getCurrentChapterId()
        item_name_text_id = TEXT_ITEM_NAME_TEMPLATE.format(chapter_id, self.item_name, TEXT_ITEM_NAME_ANNEX)
        self.title_text_id = item_name_text_id

    def _setupItemDescriptionFull(self):
        self.text_description_full = Mengine.createNode("TextField")
        self.text_description_full.setName(self.item_name + "_" + TEXT_ITEM_DESCRIPTION_FULL_ANNEX)

        self.text_description_full.setVerticalCenterAlign()
        self.text_description_full.setHorizontalCenterAlign()

        self.text_description_full.setJustify(True)

        self.text_description_full.setTextId(TEXT_ITEM_DESCRIPTION_FULL)

        chapter_id = GameManager.getCurrentChapterId()
        item_description_full_text_id = TEXT_ITEM_DESCRIPTION_FULL_TEMPLATE.format(chapter_id, self.item_name, TEXT_ITEM_DESCRIPTION_FULL_ANNEX)
        item_description_full_text = Mengine.getTextFromId(item_description_full_text_id)
        self.text_description_full.setTextFormatArgs(item_description_full_text)

        slot = self.content.getMovieSlot(SLOT_ITEM_DESCRIPTION)
        slot.addChild(self.text_description_full)

        popup_content_size = self.pop_up_base.getContentSize()

        self.text_description_full.setMaxLength(popup_content_size.x)

        self.text_description_full.enable()

    def _setupLayoutBox(self):
        item_sprite_wrapper = LayoutSpriteWrapper(self.item_sprite)
        item_description_full_wrapper = LayoutTextWrapper(self.text_description_full)

        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            vertical.addPadding(1)
            vertical.addFixedObject(item_sprite_wrapper)
            vertical.addPadding(1)
            vertical.addFixedObject(item_description_full_wrapper)
            vertical.addPadding(1)
