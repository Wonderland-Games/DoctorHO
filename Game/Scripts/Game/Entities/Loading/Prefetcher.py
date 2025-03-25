from Foundation.Systems.SystemAnalytics import SystemAnalytics
from Foundation.PrefetchGroupNotifyManager import PrefetchGroupNotifyManager


class Prefetcher(object):

    def __init__(self, owner):
        self.owner = owner

    def scopePrefetchScripts(self, source, progress_value):
        def __prefetchScripts(isSkip, cb):
            def __done(isDone):
                if isDone is True:
                    SystemAnalytics.sendCustomAnalytic("prefetch_scripts_success", {})
                else:
                    SystemAnalytics.sendCustomAnalytic("prefetch_scripts_fail", {})
                cb(isSkip)
            if Mengine.prefetchScripts(__done) is False:
                cb(isSkip)

        source.addFunction(SystemAnalytics.sendCustomAnalytic, "prefetch_scripts_begin", {})
        source.addCallback(__prefetchScripts)
        # source.addPrint(" SCRIPTS PREFETCHED")

        source.addFunction(self.owner.addLoadingProgress, progress_value)

    def scopePrefetchFonts(self, source, progress_value):
        def __prefetchFonts(isSkip, cb):
            def __done(isDone):
                if isDone is True:
                    SystemAnalytics.sendCustomAnalytic("prefetch_fonts_success", {})
                else:
                    SystemAnalytics.sendCustomAnalytic("prefetch_fonts_fail", {})
                cb(isSkip)
            if Mengine.prefetchFonts(__done) is False:
                cb(isSkip)

        source.addFunction(SystemAnalytics.sendCustomAnalytic, "prefetch_fonts_begin", {})
        source.addCallback(__prefetchFonts)
        # source.addPrint(" FONTS PREFETCHED")

        source.addFunction(self.owner.addLoadingProgress, progress_value)

    def scopePrefetchGroups(self, source, progress_value):
        source.addFunction(SystemAnalytics.sendCustomAnalytic, "prefetch_groups_begin", {})

        if PrefetchGroupNotifyManager.isPrefetchFinished() is True:
            source.addFunction(self.owner.addLoadingProgress, progress_value)
        else:
            prefetch_groups = PrefetchGroupNotifyManager.getPrefetchGroup(None)

            if len(prefetch_groups) == 0:
                source.addFunction(self.owner.addLoadingProgress, progress_value)
                return

            def __prefetchGroups(prefetch_source):
                prefetch_group_progress_value_part = float(progress_value) / len(prefetch_groups)
                prefetch_group_progress_value_part = round(prefetch_group_progress_value_part+0.1, 1)   # bad fix
                for _ in prefetch_groups:
                    prefetch_source.addListener(Notificator.onPrefetchGroupsTaggedComplete)
                    prefetch_source.addFunction(self.owner.addLoadingProgress, prefetch_group_progress_value_part)

            source.addForkScope(__prefetchGroups)
            source.addListener(Notificator.onPrefetchGroupsTaggedFinished)

        source.addFunction(SystemAnalytics.sendCustomAnalytic, "prefetch_groups_complete", {})
