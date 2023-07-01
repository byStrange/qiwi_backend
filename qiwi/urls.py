from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def testCheck(request):
    if request.method == "POST":
        data = json.load(request)["data"]
        print(data)
        return JsonResponse({"status": "OK"})


urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("testCheck/", testCheck),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
