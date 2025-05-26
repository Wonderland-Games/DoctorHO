from Foundation.Group import Group

class GroupIntro(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Movie2", Name = "Movie2_Cutscene" , ResourceMovie = "Movie2_Intro", CompositionName = "Cutscene"  )
        self.createObject( "Movie2", Name = "Movie2_Play_1" , ResourceMovie = "Movie2_Intro", CompositionName = "Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Loop_1" , ResourceMovie = "Movie2_Intro", CompositionName = "Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Play_2" , ResourceMovie = "Movie2_Intro", CompositionName = "Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Loop_2" , ResourceMovie = "Movie2_Intro", CompositionName = "Loop_2"  )
        pass
    pass
