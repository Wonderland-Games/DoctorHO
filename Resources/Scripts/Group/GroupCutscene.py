from Foundation.Group import Group

class GroupCutscene(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Cutscene", Name = "Demon_Cutscene" )
        def setup_Demon_Cutscene(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_Cutscene", CompositionName = "Content"  )
            pass
        Demon_Cutscene = self.getObject( "Demon_Cutscene")
        setup_Demon_Cutscene(Demon_Cutscene)
        pass
    pass
