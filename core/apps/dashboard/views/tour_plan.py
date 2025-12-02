# django
from django.db.models import Q

# rest framework
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# dashboard
from core.apps.dashboard.serializers import tour_plan as serializers

# shared
from core.apps.shared.models import TourPlan
from core.apps.shared.utils.response_mixin import ResponseMixin


class TourPlanViewSet(viewsets.GenericViewSet, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]
    queryset = TourPlan.objects.all()

    def get_serializer_class(self):
        match self.action: 
            case "post": 
                return serializers.TourPlanCreateSerializer
            case "update_doctor":
                return serializers.AdminTourPlanUpdateSerializer
            case _:
                return serializers.AdminTourPlanListSerializer

    @swagger_auto_schema(
        tags=['Admin Tour Plans'],
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="name",
                description="place name bo'yicha filter",
                required=False,
                type=openapi.TYPE_STRING,
            ),
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
                description="tanlangan foydalanuvchini ism va familiyasi bo'yicha qidirish",
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
            date = request.query_params.get('date', None)
            user_full_name = request.query_params.get('user', None)

            queryset = self.queryset.all()

            # filters
            if name is not None:
                queryset = queryset.filter(place_name__istartswith=name)
            
            if date is not None:
                queryset = queryset.filter(date=date)
            
            if user_full_name is not None:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=user_full_name) |
                    Q(user__last_name__istartswith=user_full_name) 
                )

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
        tags=['Admin Tour Plans']
    )
    @action(detail=False, methods=['post'], url_path='create')
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.TourPlanListSerializer(obj).data,
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
        tags=['Admin Tour Plans']
    )
    @action(detail=True, methods=['patch'], url_path='update')
    def update_doctor(self, request, pk=None):
        try:
            tour_plan = TourPlan.objects.filter(id=pk).first()
            if not tour_plan:
                return self.failure_response(
                    data={},
                    message="tour_plan topilmadi",
                    status_code=404
                )
            serializer = self.get_serializer(data=request.data, instance=tour_plan)
            if serializer.is_valid():
                obj = serializer.save()
                return self.success_response(
                    data=serializers.TourPlanListSerializer(obj).data,
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
        tags=['Admin Tour Plans']
    )
    @action(detail=True, methods=['delete'], url_path='delete')
    def delete(self, request, pk=None):
        try:
            tour_plan = TourPlan.objects.filter(id=pk).first()
            if not tour_plan:
                return self.failure_response(
                    data={},
                    message="tour_plan topilmadi",
                    status_code=404
                )
            tour_plan.delete()
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
    
    