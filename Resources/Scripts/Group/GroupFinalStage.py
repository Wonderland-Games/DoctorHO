from Foundation.Group import Group

class GroupFinalStage(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "FinalStage", Name = "Demon_FinalStage" )
        def setup_Demon_FinalStage(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_FinalStage", CompositionName = "Content"  )
            self.createObject( "Movie2", Name = "Movie2_DropPanel" , ResourceMovie = "Movie2_FinalStage", CompositionName = "DropPanel"  )
            pass
        Demon_FinalStage = self.getObject( "Demon_FinalStage")
        setup_Demon_FinalStage(Demon_FinalStage)
        pass
    pass
