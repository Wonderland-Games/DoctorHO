from Foundation.Group import Group

class Group02_Venus(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", Position = (600,0), SpriteResourceName = "02_Venus/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Item", Name = "Item_Notebook", Position = (1669,931), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Notebook/_Item_Notebook[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Notebook/_Item_Notebook[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Binoculars", Position = (1499,967), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Binoculars/_Item_Binoculars[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Binoculars/_Item_Binoculars[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Helmet", Position = (1301,944), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Helmet/_Item_Helmet[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Helmet/_Item_Helmet[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Backpack", Position = (1092,916), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Backpack/_Item_Backpack[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Backpack/_Item_Backpack[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Phone", Position = (829,914), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Phone/_Item_Phone[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Phone/_Item_Phone[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Respirator", Position = (1707,708), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Respirator/_Item_Respirator[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Respirator/_Item_Respirator[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Drone", Position = (1443,670), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Drone/_Item_Drone[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Drone/_Item_Drone[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Pistol", Position = (1281,706), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Pistol/_Item_Pistol[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Pistol/_Item_Pistol[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Quest_Gun", Position = (1031,732), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Quest_Gun/_Item_Quest_Gun[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Quest_Gun/_Item_Quest_Gun[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Sword", Position = (787,663), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Sword/_Item_Sword[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Sword/_Item_Sword[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Robot", Position = (1690,378), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Robot/_Item_Robot[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Robot/_Item_Robot[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Boots", Position = (1528,444), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Boots/_Item_Boots[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Boots/_Item_Boots[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Armor", Position = (1282,410), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Armor/_Item_Armor[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Armor/_Item_Armor[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Spaceship", Position = (1035,442), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Spaceship/_Item_Spaceship[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Spaceship/_Item_Spaceship[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Clock", Position = (864,438), SpriteResourceNameFull = "02_Venus/Layer2D_Main/Item_Clock/_Item_Clock[Full]" , HotspotImageResourceName = "02_Venus/Layer2D_Main/Item_Clock/_Item_Clock[Pick]", PickOffset = (0, 0) )
        pass
    pass
