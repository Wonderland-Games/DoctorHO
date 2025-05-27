from Foundation.Manager import Manager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.GroupManager import GroupManager


class CutsceneManager(Manager):
    _cutscenes = {}

    class Cutscene(object):
        def __init__(self, cutscene_id, cutscene_group_name, cutscene_movies):
            self.cutscene_id = cutscene_id
            self.cutscene_group_name = cutscene_group_name
            self.cutscene_movies = cutscene_movies

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)
        for record in records:
            cutscene_id = record.get("CutsceneId")
            cutscene_group_name = record.get("CutsceneGroupName")
            cutscene_movies = record.get("CutsceneMovies", [])

            if GroupManager.hasGroup(cutscene_group_name) is False:
                Trace.msg_err("CutsceneManager.loadParams: invalid add cutscene {!r}, not found group {!r}"
                              .format(cutscene_id, cutscene_group_name))
                continue

            cutscene = CutsceneManager.Cutscene(cutscene_id, cutscene_group_name, cutscene_movies)
            CutsceneManager._cutscenes[cutscene_id] = cutscene

        return True

    @staticmethod
    def getCutscene(cutscene_id):
        cutscene = CutsceneManager._cutscenes.get(cutscene_id)
        if cutscene is None:
            Trace.msg_err("CutsceneManager.getCutscene: invalid cutscene id {!r}".format(cutscene_id))
            return None

        return cutscene
