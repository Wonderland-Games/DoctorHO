from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class QuestItemReceived(PopUpContent):
    content_id = "QuestItemReceived"
    title_text_id = "ID_PopUpTitle_" + content_id
    content_movie_name = "Movie2_Content_" + content_id

    def __init__(self):
        super(QuestItemReceived, self).__init__()
        pass

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(QuestItemReceived, self)._onInitializeContent()
        pass

    def _onFinalizeContent(self):
        super(QuestItemReceived, self)._onFinalizeContent()
        pass
