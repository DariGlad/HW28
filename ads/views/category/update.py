import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from ads.models import Category


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = [
        "name"
    ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        if "name" in data.keys():
            self.object.name = data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name
        }, safe=False)
