import fcntl
import struct
from django.views.generic import TemplateView
import qrcode
import qrcode.image.svg
import socket
import base64
from io import BytesIO
import uuid

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

class DomView(TemplateView):
    template_name = "dom-view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DomView, self).get_context_data(*args, **kwargs)
        factory = qrcode.image.svg.SvgImage
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        data = self.request.scheme + "://" + s.getsockname()[0] + ":" + self.request.META['SERVER_PORT'] + "/pair?code=" + str(uuid.uuid4())
        s.close()
        qr_image = qrcode.make(data, image_factory=factory,)
        stream = BytesIO()
        qr_image.save(stream)
        
        context['svg'] = stream.getvalue().decode()
        context['data'] = data
        return context

class PairDeviceView(TemplateView):
    template_name = "pair-device-view.html"

class ControlSubView(TemplateView):
    template_name = "control-sub-view.html"