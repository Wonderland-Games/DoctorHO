from Foundation.Group import Group

class GroupQuestItemStore_Ancient(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2560,2560), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2560, 2560), Main = True )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Armor", Position = (43,0), SpriteResourceName = "QuestItemStore_Ancient/Layer2D_Main/Sprite_Item_Quest_Armor/Sprite_Item_Quest_Armor" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Helmet", Position = (568,0), SpriteResourceName = "QuestItemStore_Ancient/Layer2D_Main/Sprite_Item_Quest_Helmet/Sprite_Item_Quest_Helmet" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Bust", Position = (1107,0), SpriteResourceName = "QuestItemStore_Ancient/Layer2D_Main/Sprite_Item_Quest_Bust/Sprite_Item_Quest_Bust" )
        pass
    pass
