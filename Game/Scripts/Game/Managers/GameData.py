class ChapterData(object):
    def __init__(self, chapter_name):
        self.chapter_name = chapter_name
        self.current_levels = []

    def getChapterName(self):
        return self.chapter_name

    def getCurrentLevels(self):
        return self.current_levels


class PlayerGameData(object):
    def __init__(self):
        self.current_chapter = None
        self._last_level_data = {}

    def getCurrentChapterData(self):
        return self.current_chapter

    def loadData(self, active_chapter_name, active_levels_names):
        self.current_chapter = ChapterData(active_chapter_name)
        self.current_chapter.current_levels = active_levels_names

    def setLastLevelData(self, value):
        self._last_level_data = value

    def getLastLevelData(self):
        return self._last_level_data
