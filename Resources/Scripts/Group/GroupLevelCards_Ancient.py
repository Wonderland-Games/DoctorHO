from Foundation.Group import Group

class GroupLevelCards_Ancient(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Active" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientEgypt_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Unlocking" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientEgypt_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Blocked" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientEgypt_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Active" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientGreece_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Unlocking" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientGreece_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Blocked" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientGreece_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Active" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientRome_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Unlocking" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientRome_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Blocked" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "01_AncientRome_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "ChapterSlots"  )
        self.addPrototype( "Movie2", Name = "Movie2_Card" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "Card"  )
        self.addPrototype( "Movie2", Name = "Movie2_QuestIndicator" , ResourceMovie = "Movie2_LevelCards_Ancient", CompositionName = "QuestIndicator"  )
        self.addPrototype( "Movie2ProgressBar", Name = "Movie2ProgressBar_Quest", ResourceMovie = "Movie2_LevelCards_Ancient", CompositionNameIdle = "Quest_Idle", CompositionNameOver = "Quest_Over", CompositionNameProgress = "Quest_Progress", CompositionNameBlock = "Quest_Block", CompositionNameFullProgress = "Quest_FullProgress", CompositionNameHolder = "Quest_Holder" )
        pass
    pass
