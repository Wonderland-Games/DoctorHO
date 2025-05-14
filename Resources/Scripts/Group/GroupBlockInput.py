from Foundation.Group import Group

class GroupBlockInput(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Movie2", Name = "Movie2_BlockInput", Interactive = True, Enable = False , ResourceMovie = "Movie2_BlockInput", CompositionName = "BlockInput"  )
        self.createObject( "Socket", Name = "Socket_Click", Polygon = [(-679, -900),(3541, -926),(3548, 2829),(-689, 2769)] )
        pass
    pass
