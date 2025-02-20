from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class LevelWon(PopUpContent):
    popup_id = "LevelWon"
    title_text_id = "APPLICATION_TITLE"
    content_movie_name = "Movie2_Content_" + popup_id

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
