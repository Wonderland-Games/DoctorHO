from Foundation.Group import Group

class GroupQuestItemStore_SolarSystem(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2560,2560), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2560, 2560), Main = True )
        self.addPrototype( "Item", Name = "Item_Quest_Armor", Position = (46,512), SpriteResourceNameFull = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Full]" , HotspotImageResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Helmet", Position = (552,512), SpriteResourceNameFull = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Full]" , HotspotImageResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Sword", Position = (1024,596), SpriteResourceNameFull = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Sword/_Item_Quest_Sword[Full]" , HotspotImageResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Sword/_Item_Quest_Sword[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Gun", Position = (1536,696), SpriteResourceNameFull = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Gun/_Item_Quest_Gun[Full]" , HotspotImageResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Gun/_Item_Quest_Gun[Pick]", PickOffset = (0, 0) )
        self.addPrototype( "Item", Name = "Item_Quest_Spaceship", Position = (2048,618), SpriteResourceNameFull = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Spaceship/_Item_Quest_Spaceship[Full]" , HotspotImageResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Item_Quest_Spaceship/_Item_Quest_Spaceship[Pick]", PickOffset = (0, 0) )
        pass
    pass
