from Foundation.Group import Group

class GroupLobby(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Lobby", Name = "Demon_Lobby" )
        def setup_Demon_Lobby(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_Lobby", CompositionName = "Content"  )
            pass
        Demon_Lobby = self.getObject( "Demon_Lobby")
        setup_Demon_Lobby(Demon_Lobby)
        pass
    pass
