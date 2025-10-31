from Foundation.Group import Group

class GroupQuestItemStore_SolarSystem(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2560,2560), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2560, 2560), Main = True )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Armor", Position = (46,0), SpriteResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Sprite_Item_Quest_Armor/Sprite_Item_Quest_Armor" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Helmet", Position = (552,0), SpriteResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Sprite_Item_Quest_Helmet/Sprite_Item_Quest_Helmet" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Sword", Position = (1024,84), SpriteResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Sprite_Item_Quest_Sword/Sprite_Item_Quest_Sword" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Gun", Position = (1536,184), SpriteResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Sprite_Item_Quest_Gun/Sprite_Item_Quest_Gun" )
        self.addPrototype( "Sprite", Name = "Sprite_Item_Quest_Spaceship", Position = (2048,106), SpriteResourceName = "QuestItemStore_SolarSystem/Layer2D_Main/Sprite_Item_Quest_Spaceship/Sprite_Item_Quest_Spaceship" )
        pass
    pass
