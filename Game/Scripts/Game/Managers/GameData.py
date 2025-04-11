class ChapterData(object):
    def __init__(self, chapter_id):
        self.chapter_id = chapter_id
        self.current_levels_id = []

    def getChapterId(self):
        return self.chapter_id

    def getCurrentLevelsId(self):
        return self.current_levels_id


class PlayerGameData(object):
    def __init__(self):
        self.current_chapter = None
        self._last_level_data = {}

    def getCurrentChapterData(self):
        return self.current_chapter

    def loadData(self, active_chapter_id, active_levels_id):
        self.current_chapter = ChapterData(active_chapter_id)
        self.current_chapter.current_levels_id = active_levels_id

    def setLastLevelData(self, value):
        self._last_level_data = value

    def getLastLevelData(self):
        return self._last_level_data
