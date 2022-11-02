from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from HW28.settings import TOTAL_ON_PAGE
from ads.models import Ad


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ad_qs = self.object_list.select_related("author", "category").order_by("-price")

        paginator = Paginator(ad_qs, TOTAL_ON_PAGE)

        page = request.GET.get("page")
        ads = paginator.get_page(page)
        ad_list = [
            {"id": ad.pk,
             "name": ad.name,
             "author_id": ad.author.pk,
             "author": ad.author.first_name,
             "price": ad.price,
             "is_published": ad.is_published,
             "description": ad.description,
             "category_id": ad.category.pk,
             "image": ad.image.url if ad.image else None
             }
            for ad in ads
        ]
        return JsonResponse({
            "items": ad_list,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }, safe=False)


class AdDetailView(DetailView):
    queryset = Ad.objects.select_related("author", "category")

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(
            {"id": ad.pk,
             "name": ad.name,
             "author_id": ad.author.pk,
             "author": ad.author.first_name,
             "price": ad.price,
             "is_published": ad.is_published,
             "description": ad.description,
             "category_id": ad.category.pk,
             "image": ad.image.url if ad.image else None
             }, safe=False
        )
