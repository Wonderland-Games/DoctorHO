from Foundation.Group import Group

class Group02_Mars(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2048,2048), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2048, 2048), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", SpriteResourceName = "02_Mars/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Item", Name = "Item_Notebook", Position = (1325,1187), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Notebook/_Item_Notebook[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Notebook/_Item_Notebook[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Binoculars", Position = (1155,1223), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Binoculars/_Item_Binoculars[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Binoculars/_Item_Binoculars[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Quest_Helmet", Position = (957,1200), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Backpack", Position = (748,1172), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Backpack/_Item_Backpack[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Backpack/_Item_Backpack[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Phone", Position = (485,1170), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Phone/_Item_Phone[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Phone/_Item_Phone[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Respirator", Position = (1363,964), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Respirator/_Item_Respirator[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Respirator/_Item_Respirator[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Drone", Position = (1099,926), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Drone/_Item_Drone[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Drone/_Item_Drone[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Pistol", Position = (937,962), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Pistol/_Item_Pistol[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Pistol/_Item_Pistol[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Gun", Position = (687,988), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Gun/_Item_Gun[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Gun/_Item_Gun[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Sword", Position = (443,919), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Sword/_Item_Sword[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Sword/_Item_Sword[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Robot", Position = (1346,634), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Robot/_Item_Robot[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Robot/_Item_Robot[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Boots", Position = (1184,700), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Boots/_Item_Boots[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Boots/_Item_Boots[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Armor", Position = (938,666), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Armor/_Item_Armor[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Armor/_Item_Armor[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Spaceship", Position = (691,698), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Spaceship/_Item_Spaceship[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Spaceship/_Item_Spaceship[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Clock", Position = (520,694), SpriteResourceNameFull = "02_Mars/Layer2D_Main/Item_Clock/_Item_Clock[Full]" , HotspotImageResourceName = "02_Mars/Layer2D_Main/Item_Clock/_Item_Clock[Pick]", PickOffset = (0, 0) )
        pass
    pass
