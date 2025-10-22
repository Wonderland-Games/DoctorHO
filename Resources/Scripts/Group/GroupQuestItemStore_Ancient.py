from Foundation.Group import Group

class GroupQuestItemStore_Ancient(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2560,2560), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2560, 2560), Main = True )
        self.addPrototype( "Item", Name = "Item_Quest_Armor", Position = (43,0), SpriteResourceNameFull = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Full]" , HotspotImageResourceName = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Helmet", Position = (568,0), SpriteResourceNameFull = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Full]" , HotspotImageResourceName = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Bust", Position = (1107,0), SpriteResourceNameFull = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Bust/_Item_Quest_Bust[Full]" , HotspotImageResourceName = "QuestItemStore_Ancient/Layer2D_Main/Item_Quest_Bust/_Item_Quest_Bust[Pick]", PickOffset = (0, 0) )
        pass
    pass
