from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
   # path('test/', views.userr),
    path('auth/', views.login),
    path('user_detail/', views.UserDetail.as_view()),
    path('post_rea/', views.PostRea.as_view()),
    path('reas_of_user/', views.ReasOfUser.as_view()),
    path('favs_of_user/', views.FavsOfUser.as_view()),
    path('search_for_reas/', views.SearchForReas.as_view()),
    path('rea_of_id/<int:rea_id>/', views.ReaOfId.as_view()),
    path('offers_of_rea/<int:rea_id>/', views.OffersOfRea.as_view()),
    path('offers_made_by_user/', views.OffersMadeByUser.as_view()),
    path('posting_offer/<int:rea_id>/', views.PostingOffer.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)