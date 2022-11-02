from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from HW28.settings import TOTAL_ON_PAGE
from users.models import User


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user_qs = self.object_list.prefetch_related("location").order_by("username")

        user_qs = user_qs.annotate(total_ads=Count("ads"))
        paginator = Paginator(user_qs, TOTAL_ON_PAGE)

        page = request.GET.get("page")
        users = paginator.get_page(page)
        user_list = [
            {
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.location.all())),
                "total_ads": user.total_ads
            }
            for user in users
        ]
        return JsonResponse({
            "items": user_list,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }, safe=False)


class UserDetailView(DetailView):
    queryset = User.objects.prefetch_related("location")

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse(
            {
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.location.all()))
            }, safe=False
        )
