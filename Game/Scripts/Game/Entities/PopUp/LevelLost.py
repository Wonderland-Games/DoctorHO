from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class LevelLost(PopUpContent):
    popup_id = "LevelLost"
    title_text_id = "ID_PopUpTitle_LevelLost"
    content_movie_name = "Movie2_Content_" + popup_id

    def __init__(self):
        super(LevelLost, self).__init__()
        pass

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(LevelLost, self)._onInitializeContent()
        pass

    def _onFinalizeContent(self):
        super(LevelLost, self)._onFinalizeContent()
        pass
