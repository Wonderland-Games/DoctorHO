from Foundation.Group import Group

class GroupLevelCards_SolarSystem(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Active" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Europa_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Unlocking" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Europa_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Blocked" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Europa_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Active" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Mars_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Unlocking" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Mars_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Blocked" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Mars_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Active" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Titan_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Unlocking" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Titan_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Blocked" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Titan_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Active" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Venus_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Unlocking" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Venus_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Blocked" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Venus_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Active" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Moon_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Unlocking" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Moon_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Blocked" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "02_Moon_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "ChapterSlots"  )
        self.addPrototype( "Movie2", Name = "Movie2_Card" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "Card"  )
        self.addPrototype( "Movie2", Name = "Movie2_QuestIndicator" , ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionName = "QuestIndicator"  )
        self.addPrototype( "Movie2ProgressBar", Name = "Movie2ProgressBar_Quest", ResourceMovie = "Movie2_LevelCards_SolarSystem", CompositionNameIdle = "Quest_Idle", CompositionNameOver = "Quest_Over", CompositionNameProgress = "Quest_Progress", CompositionNameBlock = "Quest_Block", CompositionNameFullProgress = "Quest_FullProgress", CompositionNameHolder = "Quest_Holder" )
        pass
    pass
