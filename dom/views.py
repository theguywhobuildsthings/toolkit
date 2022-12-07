from django.views.generic import TemplateView

class DomView(TemplateView):
    template_name = "dom-view.html"

class PairDeviceView(TemplateView):
    template_name = "pair-device-view.html"

class ControlSubView(TemplateView):
    template_name = "control-sub-view.html"