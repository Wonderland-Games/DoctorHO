from Foundation.Group import Group

class Group01_FinalStage(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2048,2048), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2048, 2048), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", SpriteResourceName = "01_FinalStage/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Item", Name = "Item_Armor", Position = (938,666), SpriteResourceNameFull = "01_FinalStage/Layer2D_Main/Item_Armor/_Item_Armor[Full]" , HotspotImageResourceName = "01_FinalStage/Layer2D_Main/Item_Armor/_Item_Armor[Pick]", PickOffset = (0, 0) )
        pass
    pass
