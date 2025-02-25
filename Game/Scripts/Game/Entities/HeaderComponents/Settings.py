from MobileKit.Entities.Header.Components.ComponentContainer import ComponentContainer


class Settings(ComponentContainer):
    slot_name = "settings"
    prototype_name = "Settings"

    def _scopeComponentLogic(self, source):
        source.addNotify(Notificator.onPopUpShow, "Settings")
