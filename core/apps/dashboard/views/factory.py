# django
from django.db.models import Q

# rest framework
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# dashboard
from core.apps.dashboard.serializers import factory as serializers
# shared
from core.apps.shared.models import Factory
from core.apps.shared.utils.response_mixin import ResponseMixin


class FactoryViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = Factory.objects.all()

    def get_serializer_class(self):
        if self.action == "post": 
            return serializers.FactoryCreateSerializer
        elif self.action in ["patch", "put"]:
            return serializers.FactoryUpdateSerializer
        else:
            return serializers.FactoryListSerializer

    @swagger_auto_schema(
        tags=['Admin Factories'],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="name",
                description="name bo'yicha filter",
                required=False,
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path="list")
    def get(self, request):
        try:
            # params
            name = request.query_params.get('name', None)

            queryset = self.queryset.all()

            # filters
            if name is not None:
                queryset = queryset.filter(name__istartswith=name)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.success_response(
                    data=self.get_paginated_response(serializer.data).data,
                    message='malumotlar fetch qilindi'
                )
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                message='malumotlar fetch qilindi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )

    @swagger_auto_schema(
        tags=['Admin Factories']
    )
    @action(detail=False, methods=['post'], url_path='create')
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.FactoryListSerializer(obj).data,
                    message='malumot qoshildi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='malumot qoshilmadi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    @swagger_auto_schema(
        tags=['Admin Factories']
    )
    @action(detail=True, methods=['patch'], url_path='update')
    def update_doctor(self, request, pk=None):
        try:
            factory = Factory.objects.filter(id=pk).first()
            if not factory:
                return self.failure_response(
                    data={},
                    message="factory topilmadi",
                    status_code=404
                )
            serializer = self.get_serializer(data=request.data, instance=factory)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.FactoryListSerializer(obj).data,
                    message='malumot tahrirlandi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='malumot tahrirlandi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    @swagger_auto_schema(
        tags=['Admin Factories']
    )
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        try:
            factory = Factory.objects.filter(id=pk).first()
            if not factory:
                return self.failure_response(
                    data={},
                    message="factory topilmadi",
                    status_code=404
                )
            factory.delete()
            return self.success_response(
                data={},
                message='malumot ochirildi',
                status_code=204
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
    
    