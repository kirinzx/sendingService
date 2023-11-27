from django.urls import path
from .views import CreateListSendingView, RetrieveUpdateDestroySendingView, openapi_spec
from django.views.generic import TemplateView

urlpatterns = [
    path('sending/',CreateListSendingView.as_view({'post':'create','get':'list'})),
    path('sending/<int:pk>',RetrieveUpdateDestroySendingView.as_view()),
    path('openapi_spec', openapi_spec,name='openapi_spec'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html'
    ), name='swagger-ui'),
]