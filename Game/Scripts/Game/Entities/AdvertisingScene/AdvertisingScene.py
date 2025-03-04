from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider


MOVIE_CONTENT = "Movie2_Content"


class AdvertisingScene(BaseScopeEntity):
    @staticmethod
    def declareORM(Type):
        BaseScopeEntity.declareORM(Type)
        Type.addAction(Type, "NextScene")
        Type.addAction(Type, "AdPlacement")

    def _onPreparation(self):
        if _DEVELOPMENT is True and self.object.hasObject(MOVIE_CONTENT):
            movie = self.object.getObject(MOVIE_CONTENT)
            movie.setEnable(True)

    def _onScopeActivate(self, source):
        with source.addParallelTask(2) as (response, request):
            response.addListener(Notificator.onAdShowCompleted)

            def __showInterstitialAdvert():
                return AdvertisementProvider.showInterstitialAdvert(self.AdPlacement)

            with request.addIfTask(__showInterstitialAdvert) as (show, skip):
                skip.addNotify(Notificator.onChangeScene, self.NextScene)

        source.addDelay(1)
        source.addNotify(Notificator.onChangeScene, self.NextScene)
