from Foundation.Group import Group

class GroupCutscene_02(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.createObject( "Movie2", Name = "Movie2_Armor_Play_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Armor_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Loop_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Armor_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Play_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Armor_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Armor_Loop_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Armor_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Play_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Helmet_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Loop_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Helmet_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Play_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Helmet_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Helmet_Loop_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Helmet_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Sword_Play_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Sword_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Sword_Loop_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Sword_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Sword_Play_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Sword_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Sword_Loop_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Sword_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Gun_Play_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Gun_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Gun_Loop_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Gun_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Gun_Play_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Gun_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Gun_Loop_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Gun_Loop_2"  )
        self.createObject( "Movie2", Name = "Movie2_Spaceship_Play_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Spaceship_Play_1"  )
        self.createObject( "Movie2", Name = "Movie2_Spaceship_Loop_1" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Spaceship_Loop_1"  )
        self.createObject( "Movie2", Name = "Movie2_Spaceship_Play_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Spaceship_Play_2"  )
        self.createObject( "Movie2", Name = "Movie2_Spaceship_Loop_2" , ResourceMovie = "Movie2_Cutscene_02", CompositionName = "Spaceship_Loop_2"  )
        pass
    pass
