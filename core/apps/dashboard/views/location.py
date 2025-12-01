# django
from django.db.models import Q

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# rest framework
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# dashboard
from core.apps.dashboard.serializers import location as serializers

# shared
from core.apps.shared.models import Location, UserLocation
from core.apps.shared.utils.response_mixin import ResponseMixin


class LocationViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = Location.objects.all()

    def get_serializer_class(self):
        return serializers.LocationListSerializer

    @swagger_auto_schema(
        tags=["Admin Location"],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="date",
                description="date bo'yicha filter",
                required=False,
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="user",
                description="qo'shgan foydalanuvchini ism va familiyasi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="list")
    def get(self, request):
        try:
            # params
            date = request.query_params.get("date", None)
            user_full_name = request.query_params.get("user", None)

            queryset = self.queryset.all()

            # filters
            if date is not None:
                queryset = queryset.filter(created_at__date=date)

            if user_full_name is not None:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=user_full_name)
                    | Q(user__last_name__istartswith=user_full_name)
                )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message="malumotlar fetch qilindi",
                )
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data, message="malumotlar fetch qilindi"
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")

    @swagger_auto_schema(tags=["Admin Location"])
    @action(detail=True, methods=["delete"], url_path="delete")
    def delete(self, request, pk=None):
        try:
            location = Location.objects.filter(id=pk).first()
            if not location:
                return self.failure_response(
                    data={}, message="location topilmadi", status_code=404
                )
            location.delete()
            return self.success_response(
                data={}, message="malumot ochirildi", status_code=204
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")


class UserLocationViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = UserLocation.objects.all()

    def get_serializer_class(self):
        return serializers.UserLocationListSerializer

    @swagger_auto_schema(
        tags=["Admin Location"],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="date",
                description="date bo'yicha filter",
                required=False,
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="user",
                description="qo'shgan foydalanuvchini ism va familiyasi bo'yicha qidirish",
                required=False,
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="list")
    def get(self, request):
        try:
            # params
            date = request.query_params.get("date", None)
            user_full_name = request.query_params.get("user", None)

            queryset = self.queryset.all()

            # filters
            if date is not None:
                queryset = queryset.filter(created_at__date=date)

            if user_full_name is not None:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=user_full_name)
                    | Q(user__last_name__istartswith=user_full_name)
                )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message="malumotlar fetch qilindi",
                )
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data, message="malumotlar fetch qilindi"
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")

    @swagger_auto_schema(tags=["Admin Location"])
    @action(detail=True, methods=["delete"], url_path="delete")
    def delete(self, request, pk=None):
        try:
            location = UserLocation.objects.filter(id=pk).first()
            if not location:
                return self.failure_response(
                    data={}, message="location topilmadi", status_code=404
                )
            location.delete()
            return self.success_response(
                data={}, message="malumot ochirildi", status_code=204
            )
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")
