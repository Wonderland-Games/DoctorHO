from Foundation.Group import Group

class GroupMissClick(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "MissClick", Name = "Demon_MissClick" )
        def setup_Demon_MissClick(self):
            self.addPrototype( "Movie2", Name = "Movie2_MissClickEffect_Show" , ResourceMovie = "Movie2_MissClick", CompositionName = "MissClickEffect_Show"  )
            self.addPrototype( "Movie2", Name = "Movie2_MissClickEffect_Idle", Play = True, Loop = True , ResourceMovie = "Movie2_MissClick", CompositionName = "MissClickEffect_Idle"  )
            self.addPrototype( "Movie2", Name = "Movie2_MissClickEffect_Hide" , ResourceMovie = "Movie2_MissClick", CompositionName = "MissClickEffect_Hide"  )
            pass
        Demon_MissClick = self.getObject( "Demon_MissClick")
        setup_Demon_MissClick(Demon_MissClick)
        self.createObject( "Socket", Name = "Socket_Block", Interactive = False, Global = True )
        pass
    pass
