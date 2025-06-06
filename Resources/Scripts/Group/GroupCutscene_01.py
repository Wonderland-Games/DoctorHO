from Foundation.Group import Group

class GroupCutscene_01(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Movie2", Name = "Movie2_Armor_Play_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Armor_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Loop_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Armor_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Play_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Armor_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Loop_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Armor_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Play_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Helmet_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Loop_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Helmet_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Play_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Helmet_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Loop_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Helmet_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Bust_Play_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Bust_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Bust_Loop_1" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Bust_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Bust_Play_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Bust_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Bust_Loop_2" , ResourceMovie = "Movie2_Cutscene_01", CompositionName = "Bust_Loop_2"  )
        pass
    pass
