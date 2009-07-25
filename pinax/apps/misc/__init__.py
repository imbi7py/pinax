from django.conf import settings
from django.core import signals
import re
MASK_IN_EXCEPTION_EMAIL= ['password', 'mail', 'protected', 'private' ]

mask_re = re.compile('(' + '|'.join(MASK_IN_EXCEPTION_EMAIL) + ')', re.I)

def clean_request_for_except_repr(signal=None, sender=None, request=None, **kwargs):
    if not request or not request.POST or settings.DEBUG: return False
    masked = False
    mutable = True
    if hasattr(request.POST, '_mutable'):
        mutable = request.POST._mutable
        request.POST._mutable = True
    for name in request.POST:
        if mask_re.search(name):
            request.POST[name]=u'xxHIDDENxx'
            masked=True
    if hasattr(request.POST, '_mutable'):
        request.POST._mutable = mutable
    return masked

signals.got_request_exception.connect(clean_request_for_except_repr)
