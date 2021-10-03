from rest_framework.viewsets import ModelViewSet
from .serializers import (
    Inventory, InventorySerializer, InventoryGroupSerializer, InventoryGroup,
    Shop, ShopSerializer, Invoice, InvoiceSerializer
)
from rest_framework.response import Response
from inventory_api.custom_methods import IsAuthenticatedCustom
from inventory_api.utils import CustomPagination, get_query
from django.db.models import Count
from user_control.views import add_user_activity



class InventoryView(ModelViewSet):
    queryset = Inventory.objects.select_related("group", "created_by")
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page")
        keyword = data.pop("keyword", None)

        results = self.queryset(**data)

        if keyword:
            search_fields = (
                "code", "created_by__fullname", "created_by__email", 
                "group__name", "name"
            )
            query = get_query(keyword, search_fields)
            return results.filter(query)
        
        return results


    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related(
        "belongs_to", "created_by").prefetch_related("inventories")
    serializer_class = InventoryGroupSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page")
        keyword = data.pop("keyword", None)

        results = self.queryset(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        
        
        return results.annotate(
            total_items = Count('inventories')
        )

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)


class ShopView(ModelViewSet):
    queryset = Shop.objects.select_related("created_by")
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page")
        keyword = data.pop("keyword", None)

        results = self.queryset(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)


class InvoiceView(ModelViewSet):
    queryset = Invoice.objects.select_related(
        "created_by", "shop").prefetch_related("invoice_items")
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page")
        keyword = data.pop("keyword", None)

        results = self.queryset(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "shop__name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id":request.user.id})
        return super().create(request, *args, **kwargs)