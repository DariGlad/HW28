import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from ads.models import Ad


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = [
        "name",
        "author",
        "price",
        "description",
        "category",
        "is_published"
    ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        if "name" in data.keys():
            self.object.name = data["name"]
        if "price" in data.keys():
            self.object.price = data["price"]
        if "description" in data.keys():
            self.object.description = data["description"]
        if "is_published" in data.keys():
            self.object.is_published = data["is_published"]

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "is_published": self.object.is_published
        }, safe=False)
