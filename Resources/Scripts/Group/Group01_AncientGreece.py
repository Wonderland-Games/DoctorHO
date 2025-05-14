from Foundation.Group import Group

class Group01_AncientGreece(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", SpriteResourceName = "01_AncientGreece/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Item", Name = "Item_Jug", Position = (1669,960), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Jug/_Item_Jug[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Jug/_Item_Jug[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Spoon", Position = (1540,953), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Spoon/_Item_Spoon[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Spoon/_Item_Spoon[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Scroll", Position = (1283,949), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Scroll/_Item_Scroll[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Scroll/_Item_Scroll[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Bust", Position = (1095,960), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Bust/_Item_Bust[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Bust/_Item_Bust[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Quest_Helmet", Position = (871,944), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Quest_Helmet/_Item_Quest_Helmet[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Sword", Position = (1671,671), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Sword/_Item_Sword[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Sword/_Item_Sword[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Food", Position = (1448,652), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Food/_Item_Food[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Food/_Item_Food[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Torch", Position = (1332,671), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Torch/_Item_Torch[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Torch/_Item_Torch[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Bow", Position = (1076,677), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Bow/_Item_Bow[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Bow/_Item_Bow[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Armor", Position = (867,647), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Armor/_Item_Armor[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Armor/_Item_Armor[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Harp", Position = (1711,378), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Harp/_Item_Harp[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Harp/_Item_Harp[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Shoes", Position = (1479,394), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Shoes/_Item_Shoes[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Shoes/_Item_Shoes[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Necklace", Position = (1290,410), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Necklace/_Item_Necklace[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Necklace/_Item_Necklace[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Staff", Position = (1107,349), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Staff/_Item_Staff[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Staff/_Item_Staff[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Crown", Position = (900,431), SpriteResourceNameFull = "01_AncientGreece/Layer2D_Main/Item_Crown/_Item_Crown[Full]" , HotspotImageResourceName = "01_AncientGreece/Layer2D_Main/Item_Crown/_Item_Crown[Pick]", PickOffset = (0, 0) )
        pass
    pass
