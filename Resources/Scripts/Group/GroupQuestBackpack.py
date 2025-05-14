from Foundation.Group import Group

class GroupQuestBackpack(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "QuestBackpack", Name = "Demon_QuestBackpack" )
        def setup_Demon_QuestBackpack(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_QuestBackpack", CompositionName = "Content"  )
            self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_Ancient" , ResourceMovie = "Movie2_QuestBackpack", CompositionName = "ChapterSlots_Ancient"  )
            self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_SolarSystem" , ResourceMovie = "Movie2_QuestBackpack", CompositionName = "ChapterSlots_SolarSystem"  )
            pass
        Demon_QuestBackpack = self.getObject( "Demon_QuestBackpack")
        setup_Demon_QuestBackpack(Demon_QuestBackpack)
        pass
    pass
