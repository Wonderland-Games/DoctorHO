from Foundation.Group import Group

class Group01_AncientEgypt(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2048,2048), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2048, 2048), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", SpriteResourceName = "01_AncientEgypt/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Item", Name = "Item_Jug", Position = (1325,1216), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Jug/_Item_Jug[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Jug/_Item_Jug[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Spoon", Position = (1196,1209), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Spoon/_Item_Spoon[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Spoon/_Item_Spoon[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Scroll", Position = (939,1205), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Scroll/_Item_Scroll[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Scroll/_Item_Scroll[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Bust", Position = (751,1216), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Bust/_Item_Bust[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Bust/_Item_Bust[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Helmet", Position = (527,1200), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Helmet/_Item_Helmet[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Helmet/_Item_Helmet[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Sword", Position = (1327,927), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Sword/_Item_Sword[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Sword/_Item_Sword[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Food", Position = (1104,908), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Food/_Item_Food[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Food/_Item_Food[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Torch", Position = (988,927), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Torch/_Item_Torch[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Torch/_Item_Torch[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Bow", Position = (732,933), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Bow/_Item_Bow[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Bow/_Item_Bow[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Quest_Armor", Position = (523,903), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Quest_Armor/_Item_Quest_Armor[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Harp", Position = (1367,634), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Harp/_Item_Harp[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Harp/_Item_Harp[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Shoes", Position = (1135,650), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Shoes/_Item_Shoes[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Shoes/_Item_Shoes[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Necklace", Position = (946,666), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Necklace/_Item_Necklace[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Necklace/_Item_Necklace[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Staff", Position = (763,605), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Staff/_Item_Staff[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Staff/_Item_Staff[Pick]", PickOffset = (0, 0) )
        self.createObject( "Item", Name = "Item_Crown", Position = (556,687), SpriteResourceNameFull = "01_AncientEgypt/Layer2D_Main/Item_Crown/_Item_Crown[Full]" , HotspotImageResourceName = "01_AncientEgypt/Layer2D_Main/Item_Crown/_Item_Crown[Pick]", PickOffset = (0, 0) )
        pass
    pass
