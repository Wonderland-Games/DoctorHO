from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.GroupManager import GroupManager


class CutsceneManager(Manager):
    _cutscenes = {}

    class Cutscene(object):
        def __init__(self, cutscene_id, cutscene_group_name):
            self.cutscene_id = cutscene_id
            self.cutscene_group_name = cutscene_group_name

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)
        for record in records:
            cutscene_id = record.get("CutsceneId")
            cutscene_group_name = record.get("CutsceneGroupName")

            if GroupManager.hasGroup(cutscene_group_name) is False:
                Trace.msg_err("CutsceneManager loadParams: invalid add cutscene {!r}, not found group {!r}"
                              .format(cutscene_id, cutscene_group_name))
                continue

            cutscene = CutsceneManager.Cutscene(cutscene_id, cutscene_group_name)
            CutsceneManager._cutscenes[cutscene_id] = cutscene

        return True
