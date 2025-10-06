from Foundation.DefaultManager import DefaultManager
import json

GAME_MODE_STORY = "Story"


class GameDataCompressor(object):
    @staticmethod
    def decompress(save_data):
        """ decompress save data if needed (must be json base64+lz4 string) """
        if isinstance(save_data, (str, unicode)) is True:
            data = Mengine.decompressBase64("lz4", str(save_data))
            data = json.loads(data)
            return data
        return save_data

    @staticmethod
    def compress(save_data):
        """ compress save data into json string then base64+lz4 """
        save_data = json.dumps(save_data)
        save_data = Mengine.compressBase64("lz4", save_data)
        return save_data


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

    def addQuestPoints(self, quest_points):
        self.quest_points += quest_points


class ChapterData(object):
    def __init__(self, chapter_id):
        self.chapter_id = chapter_id
        self.levels_data = {}
        self.current_quest_index = 0

    def getChapterId(self):
        return self.chapter_id

    def getCurrentQuestIndex(self):
        return self.current_quest_index

    def setCurrentQuestIndex(self, quest_index):
        self.current_quest_index = quest_index

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
    game_name = None
    version = 1

    def loadData(self, save_data):
        """ input: dict """
        return

    def saveData(self):
        """ :returns: json string """
        return "{}"


class StoryPlayerGameData(PlayerGameData):
    game_name = GAME_MODE_STORY

    def __init__(self):
        self.current_chapter = None
        self._last_level_data = {}

    def getCurrentChapterData(self):
        return self.current_chapter

    def loadData(self, save_data):
        save_version = save_data.get("__VERSION", 0)
        self.version = save_version

        story_data = save_data.get("Data", {})
        # TEMP
        active_chapter_id = story_data.get("active_chapter_id")
        active_quest_index = story_data.get("active_quest_index")
        levels_data = story_data.get("levels_data")

        self.current_chapter = ChapterData(active_chapter_id)
        self.current_chapter.current_quest_index = active_quest_index

        for level_id, level_data in levels_data.items():
            _level_data = LevelData(level_id)
            _level_data.setActive(level_data.get("Active", False))
            _level_data.setQuestPoints(level_data.get("QuestPoints", 0))
            self.current_chapter.setLevelData(level_id, _level_data)

    def saveData(self):
        save_data = {
            "Data": {
                "active_chapter_id": self.current_chapter.getChapterId(),
                "active_quest_index": self.current_chapter.getCurrentQuestIndex(),
                "levels_data": {
                    level_id: {
                        "Active": level_data.getActive(),
                        "QuestPoints": level_data.getQuestPoints(),
                    } for level_id, level_data in self.current_chapter.levels_data.items()
                },
            },
            "__VERSION": self.version,  # actual version
        }

        if DefaultManager.getDefaultBool("CompressSaveGameData", True) is True:
            save_data = GameDataCompressor.compress(save_data)

        return save_data

    def setLastLevelData(self, value):
        self._last_level_data = value

    def getLastLevelData(self):
        return self._last_level_data
