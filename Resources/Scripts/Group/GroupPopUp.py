from Foundation.Group import Group

class GroupPopUp(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "PopUp", Name = "Demon_PopUp" )
        def setup_Demon_PopUp(self):
            self.addPrototype( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_LevelLost" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_LevelLost"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_LevelWon" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_LevelWon"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_Settings" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_Settings"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_Languages" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_Languages"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_Support" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_Support"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_Credits" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_Credits"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_DebugAd" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_DebugAd"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_QuestItemReceived" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_QuestItemReceived"  )
            self.addPrototype( "Movie2", Name = "Movie2_Content_QuestItemDescription" , ResourceMovie = "Movie2_PopUp", CompositionName = "Content_QuestItemDescription"  )
            pass
        Demon_PopUp = self.getObject( "Demon_PopUp")
        setup_Demon_PopUp(Demon_PopUp)
        pass
    pass
