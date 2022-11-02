import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from ads.models import Ad, Category
from users.models import User


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = [
        "name",
        "author",
        "price",
        "description",
        "is_published"
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, username=data["author"])
        category = get_object_or_404(Category, name=data["category"])

        ad = Ad.objects.create(
            name=data["name"],
            author=author,
            category=category,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"]
        )
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "is_published": ad.is_published
        }, status=201, safe=False)
