from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class LevelWon(PopUpContent):
    content_id = "LevelWon"
    title_text_id = "ID_PopUpTitle_LevelWon"
    content_movie_name = "Movie2_Content_" + content_id

    def __init__(self):
        super(LevelWon, self).__init__()
        pass

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(LevelWon, self)._onInitializeContent()
        pass

    def _onFinalizeContent(self):
        super(LevelWon, self)._onFinalizeContent()
        pass
