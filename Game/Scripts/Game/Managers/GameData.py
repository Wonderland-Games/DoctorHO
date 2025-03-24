class LevelData(object):
    def __init__(self, level_name):
        self.level_name = level_name


class ChapterData(object):
    def __init__(self, chapter_name):
        self.chapter_name = chapter_name
        self.levels = {}
        self.current_level = None

    def getLevelData(self, level):
        return self.levels.get(level)

    def getCurrentLevelData(self):
        return self.getLevelData(self.current_level)


class PlayerGameData(object):
    def __init__(self):
        self.chapters = {}
        self.current_chapter = None

    def getChapterData(self, chapter):
        return self.chapters.get(chapter)

    def getCurrentChapterData(self):
        return self.getChapterData(self.current_chapter)
