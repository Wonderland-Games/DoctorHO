from Foundation.Group import Group

class GroupDummyBanner(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Movie2", Name = "Movie2_Banner" , ResourceMovie = "Movie2_DummyBanner", CompositionName = "Banner"  )
        pass
    pass
