from Foundation.Group import Group

class GroupLoading(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Loading", Name = "Demon_Loading" )
        def setup_Demon_Loading(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_Loading", CompositionName = "Content"  )
            pass
        Demon_Loading = self.getObject( "Demon_Loading")
        setup_Demon_Loading(Demon_Loading)
        pass
    pass
