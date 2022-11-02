import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from users.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = [
        "username",
        "first_name",
        "last_name",
        "role",
        "age",
        "location"
    ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        if "first_name" in data.keys():
            self.object.first_name = data["first_name"]
        if "last_name" in data.keys():
            self.object.last_name = data["last_name"]
        if "role" in data.keys():
            self.object.role = data["role"]
        if "age" in data.keys():
            self.object.age = data["age"]
        if "locations" in data.keys():
            for loc_name in data["locations"]:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "username": self.object.username,
            "password": self.object.password,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.location.all()))
        }, safe=False)
