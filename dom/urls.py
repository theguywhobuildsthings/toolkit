from django.urls import path

from dom.views import DomView, PairDeviceView, ControlSubView

app_name = 'dom'

urlpatterns = [
    path('', DomView.as_view(), name="dom-view"),
    path('pair-device', PairDeviceView.as_view(), name="pair-device"),
    path('control-sub', ControlSubView.as_view(), name="control-sub"),

]