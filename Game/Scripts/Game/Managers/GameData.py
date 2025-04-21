class LevelData(object):
    def __init__(self, level_id):
        self.level_id = level_id
        self.active = False
        self.quest_points = 0

    def getLevelId(self):
        return self.level_id

    def getActive(self):
        return self.active

    def getQuestPoints(self):
        return self.quest_points


class ChapterData(object):
    def __init__(self, chapter_id):
        self.chapter_id = chapter_id
        self.active_levels_id = []
        self.levels_data = {}
        self.current_quest_index = 0

    def getChapterId(self):
        return self.chapter_id

    def getCurrentQuestIndex(self):
        return self.current_quest_index

    def getActiveLevelsId(self):
        return self.active_levels_id

    def appendActiveLevelsId(self, level_id):
        if level_id not in self.active_levels_id:
            self.active_levels_id.append(level_id)

    def clearActiveLevelsId(self):
        self.active_levels_id = []

    def getLevelData(self, level_id):
        return self.levels_data[level_id]

    def getBlockedLevelsData(self):
        levels_data = {}
        for level_id, level_data in self.levels_data.values():
            if level_data.getActive() is False:
                levels_data[level_id] = level_data

        return levels_data


class PlayerGameData(object):
    def __init__(self):
        self.current_chapter = None
        self._last_level_data = {}
        self._quest_points = 0

    def getCurrentChapterData(self):
        return self.current_chapter

    def loadData(self, active_chapter_id, active_levels_id, active_quest_index, quest_points):
        self.current_chapter = ChapterData(active_chapter_id)
        self.current_chapter.current_quest_index = active_quest_index
        self.current_chapter.active_levels_id = active_levels_id
        self._quest_points = quest_points

    def setLastLevelData(self, value):
        self._last_level_data = value

    def getLastLevelData(self):
        return self._last_level_data

    def getQuestPoints(self):
        return self._quest_points

    def setQuestPoints(self, value):
        self._quest_points = value

    def incQuestPoints(self, value):
        self._quest_points += value
