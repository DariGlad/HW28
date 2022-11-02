import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from users.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = [
        "username",
        "first_name",
        "last_name",
        "role",
        "age",
        "locations"
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=data["role"],
            age=data["age"]
        )

        if "locations" in data.keys():
            for loc_name in data["locations"]:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        return JsonResponse({
            "id": user.pk,
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.location.all()))
        }, status=201, safe=False)
