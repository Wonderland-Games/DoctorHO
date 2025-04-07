from UIKit.Entities.PopUp.PopUpContent import PopUpContent


AD_TIME = 3000.0


class DebugAd(PopUpContent):
    content_id = "DebugAd"

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(DebugAd, self)._onInitializeContent()
        self._runTaskChains()

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        with self._createTaskChain(self.__class__.__name__) as tc:
            tc.addDelay(AD_TIME)
            tc.addNotify(Notificator.onPopUpHide)
