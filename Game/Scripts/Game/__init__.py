def onInitialize():
    from Foundation.DefaultManager import DefaultManager

    from Foundation.Notificator import Notificator
    identities = [
        "onInternetConnectionLost",
        "onInternetConnectionFail",

        "onUserAuthBegin",
        "onUserAuthNeedRegister",
        "onUserRegistrationSuccess",
        "onUserRegistrationFail",
        "onUserAuthSuccess",
        "onUserAuthFail",

        "onLoadFromServerSuccess",
        "onLoadFromServerFail",
        "onLoadFromServerBegin",

        "onUserLinkAccount",
        "onServerMaintenance",
        "onServerUpdating",
        "onServerFail",
        "onUpdateSoft",
        "onUpdateHard",

        "onGameDataLoaded",
        "onLoadDataFromCacheBegin",
        "onLoadDataFromCacheEnd",

        "onChangeScene",

        "onLevelStart",
        "onLevelEnd",
        "onLevelMissClicked",
        "onLevelHintClicked",
        "onMissClickEffect",
        "onLevelLivesDecrease",
        "onLevelLivesChanged",
        "onLevelLivesRestore",

        "onCallRewardedAd",

        "onDisplayNameChanged",

        "onPopUpQuestItemReceived",

        "onQuestItemClicked",
    ]

    Notificator.addIdentities(identities)

    from TraceManager import TraceManager

    traces = [
    ]

    TraceManager.addTraces(traces)

    from Foundation.EntityManager import EntityManager
    from Foundation.ObjectManager import ObjectManager

    types = [
        "Loading",
        "Lobby",
        "GameArea",
        "MissClick",
        {"name": "AdvertisingScene", "override": True},
        "QuestBackpack",
        "Cutscene",
        {"name": "Header", "override": True},
        "GameHeader",
    ]

    if EntityManager.importEntities("Game.Entities", types) is False:
        return False
    if ObjectManager.importObjects("Game.Objects", types) is False:
        return False

    from UIKit.Managers.PopUpManager import PopUpManager

    pop_ups = [
        "LevelLost",
        "LevelWon",
        "Settings",
        "Languages",
        "Support",
        "Credits",
        "DebugAd",
        "QuestItemReceived",
        "QuestItemDescription",
    ]
    if PopUpManager.importPopUpContents("Game.Entities.PopUp", pop_ups) is False:
        return False

    from UIKit.AdjustableScreenUtils import AdjustableScreenUtils

    headers = [
        "Header",
        "GameHeader",
    ]
    AdjustableScreenUtils.registerHeaders(headers)

    from Foundation.AccountManager import AccountManager

    def accountSetuper(accountID, isGlobal):
        if isGlobal is True:
            return

        Mengine.addCurrentAccountSetting("FirstName", u"", None)

    AccountManager.setCreateAccount(accountSetuper)

    def onCreateDefaultAccount():
        default_account = Mengine.createAccount()
        Mengine.setDefaultAccount(default_account)
        Mengine.saveAccounts()

    AccountManager.setCreateDefaultAccount(onCreateDefaultAccount)

    from Foundation.SessionManager import SessionManager
    from GameSession import GameSession

    SessionManager.setSessionType(GameSession)
    return True


def onFinalize():
    pass
