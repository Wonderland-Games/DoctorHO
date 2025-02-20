def onInitialize():
    from Foundation.DefaultManager import DefaultManager

    from Foundation.Notificator import Notificator
    identities = [
        "onChangeScene",

        "onLevelStart",
        "onLevelEnd",
        "onLevelMissClicked",
        "onLevelHintClicked",
        "onLevelLivesDecrease",
        "onLevelLivesChanged",
    ]

    Notificator.addIdentities(identities)

    from TraceManager import TraceManager

    traces = [
    ]

    TraceManager.addTraces(traces)

    from Foundation.EntityManager import EntityManager
    from Foundation.ObjectManager import ObjectManager

    types = [
        "Lobby",
        "GameArea",
    ]

    if EntityManager.importEntities("Game.Entities", types) is False:
        return False
    if ObjectManager.importObjects("Game.Objects", types) is False:
        return False

    from UIKit.Managers.PopUpManager import PopUpManager

    pop_ups = [
        "LevelLost",
    ]
    if PopUpManager.importPopUpContents("Game.Entities.PopUp", pop_ups) is False:
        return False

    from Foundation.AccountManager import AccountManager

    def accountSetuper(accountID, isGlobal):
        if isGlobal is True:
            return

        Mengine.addCurrentAccountSetting("Default", u"False", None)
        Mengine.addCurrentAccountSetting("Save", u"False", None)
        Mengine.addCurrentAccountSetting("SessionSave", u"True", None)
        Mengine.addCurrentAccountSetting("Name", u"Player", None)
        Mengine.addCurrentAccountSetting("SelectedLanguage", u"", None)

        # SOUND\MUSIC params

        def __updateMuteMusic(account_id, value):
            if value == "True":
                Mengine.musicSetVolume(0.0)
                return
            music_volume_percent = float(Mengine.getCurrentAccountSetting("MusicVolumePercent"))
            Mengine.musicSetVolume(music_volume_percent)

        def __updateMuteSound(account_id, value):
            if value == "True":
                Mengine.soundSetVolume(0.0)
                return
            sound_volume_percent = float(Mengine.getCurrentAccountSetting("SoundVolumePercent"))
            Mengine.soundSetVolume(sound_volume_percent)

        def __updateMusicVolumePercent(account_id, value):
            if Mengine.getCurrentAccountSettingBool("MuteMusic") is False:
                Mengine.musicSetVolume(float(value))

        def __updateSoundVolumePercent(account_id, value):
            if Mengine.getCurrentAccountSettingBool("MuteSound") is False:
                Mengine.soundSetVolume(float(value))

        default_music_volume = DefaultManager.getDefaultFloat("DefaultMusicVolume", 1.0)
        default_sound_volume = DefaultManager.getDefaultFloat("DefaultSoundVolume", 1.0)

        Mengine.addCurrentAccountSetting("MuteMusic", u"False", __updateMuteMusic)
        Mengine.addCurrentAccountSetting("MuteSound", u"False", __updateMuteSound)
        Mengine.addCurrentAccountSetting("SoundVolumePercent", unicode(default_sound_volume), __updateSoundVolumePercent)
        Mengine.addCurrentAccountSetting("MusicVolumePercent", unicode(default_music_volume), __updateMusicVolumePercent)
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
