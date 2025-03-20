from Foundation.DatabaseManager import DatabaseManager
from Foundation.ObjectManager import ObjectManager


class LevelCardManager(object):
    s_db_module = "Database"
    s_db_name = "LevelCards"

    @staticmethod
    def generateObjectFromPrototypeORM(prototypeORM):
        object = ObjectManager.createObjectUnique(
            prototypeORM.Type,
            prototypeORM.Name,
            None,
            **prototypeORM.Params
        )
        return object

    @staticmethod
    def generateLevelCard(name):
        icon_db = DatabaseManager.getDatabase(
            LevelCardManager.s_db_module,
            LevelCardManager.s_db_name
        )

        if icon_db is None:  # error handled in DatabaseManager
            return None

        icon_orm = DatabaseManager.findDB(icon_db, Prototype=name)
        if icon_orm is None:
            Trace.log("Manager", 0, "[LevelCardManager|generateLevelCard]"
                                    "\n ! fail to find icon orm"
                                    "\n > Module={!r} ORM={!r} Name = {!r}"
                      .format(LevelCardManager.s_db_module, LevelCardManager.s_db_name, name))
            return None

        icon = LevelCardManager.generateObjectFromPrototypeORM(icon_orm)
        if icon is None:
            Trace.log("Manager", 0, "[LevelCardManager|generateLevelCard]"
                                    "\n ! fail to generate icon"
                                    "\n > Module={!r} ORM={!r} Name = {!r}"
                      .format(LevelCardManager.s_db_module, LevelCardManager.s_db_name, name))
            return None

        return icon

    @staticmethod
    def generateLevelCardOnNode(node, name):
        if node is None:
            Trace.log("Manager", 0, "[LevelCardManager|generateLevelCardOnNode]"
                                    "\n > node is None")
            return None

        icon = LevelCardManager.generateLevelCard(name)
        if icon is None:  # error handled in generateIcon func
            return None

        icon_node = icon.getEntityNode()
        node.addChild(icon_node)

        return icon
