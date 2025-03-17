from UIKit.Entities.PopUp.PopUpContent import PopUpContent


AD_TIME = 3000.0


class DebugAd(PopUpContent):
    content_id = "DebugAd"
    title_text_id = "ID_PopUpTitle_" + content_id
    content_movie_name = "Movie2_Content_" + content_id

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(DebugAd, self)._onInitializeContent()
        self._runTaskChains()

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        with self._createTaskChain(self.__class__.__name__) as tc:
            tc.addDelay(AD_TIME)
            tc.addNotify(Notificator.onPopUpHide)
