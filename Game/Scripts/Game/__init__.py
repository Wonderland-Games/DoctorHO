def onInitialize():
    Trace.msg_dev("Game.onInitialize")

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
        "onDropFail",
        "onDropSuccess",
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

    EntityTypes = [
        "Loading",
        "Lobby",
        "GameArea",
        "FinalStage",
        "MissClick",
        {"Type": "AdvertisingScene", "Override": True},
        "Cutscene",
        {"Type": "Header", "Override": True},
        "GameHeader",
        "QuestBackpack",
    ]

    from Foundation.Bootstrapper import Bootstrapper
    if Bootstrapper.loadEntities("Game", EntityTypes) is False:
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

    from Foundation.Managers import Managers

    Managers.importManager("Game.Managers", "GameManager")
    Managers.importManager("Game.Managers", "CutsceneManager")

    return True


def onFinalize():
    Trace.msg_dev("Game.onFinalize")

    from Foundation.Managers import Managers

    Managers.removeManager("Game.Managers", "CutsceneManager")
    Managers.removeManager("Game.Managers", "GameManager")
    pass
