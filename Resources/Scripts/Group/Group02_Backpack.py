from Foundation.Group import Group

class Group02_Backpack(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Backpack", Name = "Demon_Backpack" )
        def setup_Demon_Backpack(self):
            self.createObject( "Movie2", Name = "Movie2_Content" , ResourceMovie = "Movie2_02_Backpack", CompositionName = "Content"  )
            self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_Ancient" , ResourceMovie = "Movie2_02_Backpack", CompositionName = "ChapterSlots_Ancient"  )
            self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_SolarSystem" , ResourceMovie = "Movie2_02_Backpack", CompositionName = "ChapterSlots_SolarSystem"  )
            self.createObject( "Movie2Button", Name = "Movie2Button_FinalStageButton", ResourceMovie = "Movie2_02_Backpack", CompositionNameIdle = "FinalStageButton_Idle", CompositionNameAppear = "FinalStageButton_Appear", CompositionNameEnter = "FinalStageButton_Enter", CompositionNameOver = "FinalStageButton_Over", CompositionNameLeave = "FinalStageButton_Leave", CompositionNamePush = "FinalStageButton_Push", CompositionNamePressed = "FinalStageButton_Pressed", CompositionNameRelease = "FinalStageButton_Release", CompositionNameClick = "FinalStageButton_Click", CompositionNameBlock = "FinalStageButton_Block", CompositionNameBlockEnter = "FinalStageButton_BlockEnter", CompositionNameBlockEnd = "FinalStageButton_BlockEnd", CompositionNameSelected = "FinalStageButton_Selected", CompositionNameSelectedEnter = "FinalStageButton_SelectedEnter", CompositionNameSelectedEnd = "FinalStageButton_SelectedEnd" )
            pass
        Demon_Backpack = self.getObject( "Demon_Backpack")
        setup_Demon_Backpack(Demon_Backpack)
        pass
    pass
