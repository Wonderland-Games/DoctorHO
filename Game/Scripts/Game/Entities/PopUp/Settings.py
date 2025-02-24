from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class Settings(PopUpContent):
    popup_id = "Settings"
    title_text_id = "ID_PopUpTitle_Settings"
    content_movie_name = "Movie2_Content_" + popup_id

    def __init__(self):
        super(Settings, self).__init__()
        pass

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Settings, self)._onInitializeContent()
        pass

    def _onFinalizeContent(self):
        super(Settings, self)._onFinalizeContent()
        pass
