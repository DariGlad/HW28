from django.http import JsonResponse


def root(request):
    return JsonResponse({"result": "ok"})
