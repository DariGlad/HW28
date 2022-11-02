import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from ads.models import Category


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = [
        "name"
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        category = Category.objects.create(
            name=data["name"]
        )
        return JsonResponse({
            "id": category.pk,
            "name": category.name
        }, status=201, safe=False)
