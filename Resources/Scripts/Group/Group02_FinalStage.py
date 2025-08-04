from Foundation.Group import Group

class Group02_FinalStage(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2048,2048), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2048, 2048), Main = True )
        self.createObject( "Sprite", Name = "Sprite_Background", SpriteResourceName = "02_FinalStage/Layer2D_Main/Sprite_Background/Sprite_Background" )
        self.createObject( "Movie2", Name = "Movie2_Sword" , ResourceMovie = "Movie2_02_FinalStage", CompositionName = "Sword"  )
        self.createObject( "Movie2", Name = "Movie2_Spaceship" , ResourceMovie = "Movie2_02_FinalStage", CompositionName = "Spaceship"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet" , ResourceMovie = "Movie2_02_FinalStage", CompositionName = "Helmet"  )
        self.createObject( "Movie2", Name = "Movie2_Gun" , ResourceMovie = "Movie2_02_FinalStage", CompositionName = "Gun"  )
        self.createObject( "Movie2", Name = "Movie2_Armor" , ResourceMovie = "Movie2_02_FinalStage", CompositionName = "Armor"  )
        pass
    pass
