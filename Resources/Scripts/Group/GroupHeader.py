from Foundation.Group import Group

class GroupHeader(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Header", Name = "Demon_Header" )
        def setup_Demon_Header(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_Header", CompositionName = "Content"  )
            pass
        Demon_Header = self.getObject( "Demon_Header")
        setup_Demon_Header(Demon_Header)
        pass
    pass
