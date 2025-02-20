from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class LevelLost(PopUpContent):
    popup_id = "LevelLost"
    title_text_id = "APPLICATION_TITLE"
    content_movie_name = "Movie2_Content_LevelLost"

    def __init__(self):
        super(LevelLost, self).__init__()
        pass

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self):
        return

    def _onFinalize(self):
        pass

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        pass

    def _onActivate(self):

        self.content.setEnable(True)

    def _onDeactivate(self):

        self.content.setEnable(False)
