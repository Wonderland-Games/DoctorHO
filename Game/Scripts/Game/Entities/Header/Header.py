from Foundation.SceneManager import SceneManager
from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
from MobileKit.Entities.Header.Header import Header as HeaderBase
from MobileKit.Entities.Header.Components.Achievements import Achievements
from Game.Entities.HeaderComponents.Settings import Settings


SETTINGS_SCENE_BLACK_LIST = [
    "LoadingScene",
    "GameArea",
    # "GameOver",
    "Settings",
    "Credits",
    "Stats",
    "Languages",
    "TechSupport",
]
TITLE_SCENE_BLACK_LIST = [
    "LoadingScene",
    "GameArea",
    "Credits",
    "MainMenu",
]
ACHIEVEMENTS_SCENE_BLACK_LIST = [
    "LoadingScene",
    "GameArea",
]
GALLERY_SCENE_WHITE_LIST = [
    "MainMenu",
]

SLOT_ACHIEVEMENTS = "achievements"


class Header(HeaderBase):

    def __init__(self):
        super(Header, self).__init__()

    def _adjustSlotsPositions(self):
        viewport = Mengine.getGameViewport()
        game_width = AdjustableScreenUtils.getGameWidth()
        this_height = self.object.getHeight()

        x_center = viewport.begin.x + game_width/2
        y_center = viewport.begin.y + this_height/2
        padding = game_width*0.1

        if self.movie_content.hasSlot(Settings.slot_name):
            slot_settings = self.movie_content.getMovieSlot(Settings.slot_name)
            slot_settings.setWorldPosition(Mengine.vec2f(
                viewport.begin.x + padding, viewport.begin.y + padding
            ))

        if self.movie_content.hasSlot(SLOT_ACHIEVEMENTS):
            slot_settings = self.movie_content.getMovieSlot(SLOT_ACHIEVEMENTS)
            slot_settings.setWorldPosition(Mengine.vec2f(
                viewport.end.x - padding, viewport.begin.y + padding
            ))

    def _setup(self):
        scene_name = SceneManager.getCurrentSceneName()

        if scene_name not in SETTINGS_SCENE_BLACK_LIST and self.movie_content.hasSlot(Settings.slot_name) is True:
            settings = Settings()
            settings.onInitialize(self)
            self.content[Settings.slot_name] = settings

        if self.isAchievementsButtonEnabled() is True:
            achievements = Achievements()
            achievements.onInitialize(self)
            self.content[SLOT_ACHIEVEMENTS] = achievements

    def isAchievementsButtonEnabled(self):
        scene_name = SceneManager.getCurrentSceneName()
        current_platform = Utils.getCurrentPlatform()

        if scene_name not in ACHIEVEMENTS_SCENE_BLACK_LIST:
            if self.movie_content.hasSlot(SLOT_ACHIEVEMENTS) is False:
                return False
            if current_platform == "WINDOWS" and _DEVELOPMENT is True:
                return True
            if current_platform == "Android":
                return True

        return False
