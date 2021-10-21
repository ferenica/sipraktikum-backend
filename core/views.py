from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /media/*",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
