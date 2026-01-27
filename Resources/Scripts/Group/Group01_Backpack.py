from Foundation.Group import Group

class Group01_Backpack(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots" , ResourceMovie = "Movie2_01_Backpack", CompositionName = "ChapterSlots"  )
        self.addPrototype( "Movie2Button", Name = "Movie2Button_FinalStageButton", ResourceMovie = "Movie2_01_Backpack", CompositionNameIdle = "FinalStageButton_Idle", CompositionNameAppear = "FinalStageButton_Appear", CompositionNameEnter = "FinalStageButton_Enter", CompositionNameOver = "FinalStageButton_Over", CompositionNameLeave = "FinalStageButton_Leave", CompositionNamePush = "FinalStageButton_Push", CompositionNamePressed = "FinalStageButton_Pressed", CompositionNameRelease = "FinalStageButton_Release", CompositionNameClick = "FinalStageButton_Click", CompositionNameBlock = "FinalStageButton_Block", CompositionNameBlockEnter = "FinalStageButton_BlockEnter", CompositionNameBlockEnd = "FinalStageButton_BlockEnd", CompositionNameSelected = "FinalStageButton_Selected", CompositionNameSelectedEnter = "FinalStageButton_SelectedEnter", CompositionNameSelectedEnd = "FinalStageButton_SelectedEnd" )
        pass
    pass
