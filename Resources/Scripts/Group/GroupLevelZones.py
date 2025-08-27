from Foundation.Group import Group

class GroupLevelZones(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2048,2048), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2048, 2048), Main = True )
        self.createObject( "Sprite", Name = "Sprite_LevelZones", SpriteResourceName = "LevelZones/Layer2D_Main/Sprite_LevelZones/Sprite_LevelZones" )
        pass
    pass
