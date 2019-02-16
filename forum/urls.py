from django.urls import path
from . import views
from project import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('<int:topic_id>/', views.topic, name='topic'),
    path('<int:topic_id>/new_post/', views.new_post, name='new_post'),
    path('<int:topic_id>/new_post/<int:post_id>/', views.new_post, name='new_post'),
    path('<int:topic_id>/<int:post_id>/', views.edit_post, name='edit_post'),
    path('<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
