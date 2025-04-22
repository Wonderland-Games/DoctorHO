class LevelData(object):
    def __init__(self, level_id):
        self.level_id = level_id
        self.active = False
        self.quest_points = 0

    def getLevelId(self):
        return self.level_id

    def getActive(self):
        return self.active

    def setActive(self, active):
        self.active = active

    def getQuestPoints(self):
        return self.quest_points

    def setQuestPoints(self, quest_points):
        self.quest_points = quest_points


class ChapterData(object):
    def __init__(self, chapter_id):
        self.chapter_id = chapter_id
        self.levels_data = {}
        self.current_quest_index = 0

    def getChapterId(self):
        return self.chapter_id

    def getCurrentQuestIndex(self):
        return self.current_quest_index

    def getLevelData(self, level_id):
        return self.levels_data[level_id]

    def setLevelData(self, level_id, level_data):
        self.levels_data[level_id] = level_data

    def getActiveLevelsData(self):
        levels_data = {}
        for level_id, level_data in self.levels_data.items():
            if level_data.getActive() is True:
                levels_data[level_id] = level_data

        return levels_data

    def getBlockedLevelsData(self):
        levels_data = {}
        for level_id, level_data in self.levels_data.items():
            if level_data.getActive() is False:
                levels_data[level_id] = level_data

        return levels_data


class PlayerGameData(object):
    def __init__(self):
        self.current_chapter = None
        self._last_level_data = {}

    def getCurrentChapterData(self):
        return self.current_chapter

    def loadData(self, active_chapter_id, active_quest_index, levels_data):
        self.current_chapter = ChapterData(active_chapter_id)
        self.current_chapter.current_quest_index = active_quest_index

        for level_id, level_data in levels_data.items():
            _level_data = LevelData(level_id)
            _level_data.setActive(level_data.get("Active", False))
            _level_data.setQuestPoints(level_data.get("QuestPoints", 0))
            self.current_chapter.setLevelData(level_id, _level_data)

    def setLastLevelData(self, value):
        self._last_level_data = value

    def getLastLevelData(self):
        return self._last_level_data
