from Foundation.Group import Group

class GroupGameArea(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "GameArea", Name = "Demon_GameArea" )
        def setup_Demon_GameArea(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_GameArea", CompositionName = "Content"  )
            self.createObject( "Movie2", Name = "Movie2_SearchPanel" , ResourceMovie = "Movie2_GameArea", CompositionName = "SearchPanel"  )
            self.addPrototype( "Movie2", Name = "Movie2_HintEffect_Show" , ResourceMovie = "Movie2_GameArea", CompositionName = "HintEffect_Show"  )
            self.addPrototype( "Movie2", Name = "Movie2_HintEffect_Idle", Play = True, Loop = True , ResourceMovie = "Movie2_GameArea", CompositionName = "HintEffect_Idle"  )
            self.addPrototype( "Movie2", Name = "Movie2_HintEffect_Hide" , ResourceMovie = "Movie2_GameArea", CompositionName = "HintEffect_Hide"  )
            pass
        Demon_GameArea = self.getObject( "Demon_GameArea")
        setup_Demon_GameArea(Demon_GameArea)
        pass
    pass
