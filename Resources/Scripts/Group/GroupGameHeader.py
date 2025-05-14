from Foundation.Group import Group

class GroupGameHeader(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "GameHeader", Name = "Demon_GameHeader" )
        def setup_Demon_GameHeader(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_GameHeader", CompositionName = "Content"  )
            pass
        Demon_GameHeader = self.getObject( "Demon_GameHeader")
        setup_Demon_GameHeader(Demon_GameHeader)
        pass
    pass
