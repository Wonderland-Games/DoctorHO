from MobileKit.Entities.Header.Components.ComponentContainer import ComponentContainer


class QuestBackpack(ComponentContainer):
    slot_name = "quest_backpack"
    prototype_name = "QuestBackpack"

    def _scopeComponentLogic(self, source):
        source.addPrint("QuestBackpack")
