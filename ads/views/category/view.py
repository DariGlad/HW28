from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from ads.models import Category


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        category_qs = self.object_list.order_by("name")
        categories = category_qs.all()

        category_list = [
            {"id": category.pk,
             "name": category.name,
             }
            for category in categories
        ]
        return JsonResponse(category_list, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse(
            {"id": category.pk,
             "name": category.name,
             }, safe=False
        )
