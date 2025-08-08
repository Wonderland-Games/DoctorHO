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
        self.createObject( "Movie2", Name = "Movie2_Final" , ResourceMovie = "Movie2_01_FinalStage", CompositionName = "Final"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet" , ResourceMovie = "Movie2_01_FinalStage", CompositionName = "Helmet"  )
        self.createObject( "Movie2", Name = "Movie2_Bust" , ResourceMovie = "Movie2_01_FinalStage", CompositionName = "Bust"  )
        self.createObject( "Movie2", Name = "Movie2_Armor" , ResourceMovie = "Movie2_01_FinalStage", CompositionName = "Armor"  )
        pass
    pass
