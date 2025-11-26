# django
from django.shortcuts import get_object_or_404
# rest framework 
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Plan
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
from core.apps.shared.serializers.plan import PlanSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin



class PlanApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="date boyicha filter bor, ?date=date",
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def get(self, request):
        try:
            date = request.query_params.get('date')
            queryset = self.queryset.filter(user=request.user)
            if date:
                queryset = queryset.filter(date=date)
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')

    @swagger_auto_schema(
        responses={
            201: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )   
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                obj = serializer.save()
                created_data = PlanSerializer(obj).data
                return self.success_response(
                    data=created_data, 
                    message='malumot qoshildi', 
                    status_code=201
                )
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
    

class ComplitePlanApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = None
    queryset = Plan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return super().get_serializer_class()

    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def post(self, request, id):
        try: 
            obj = get_object_or_404(Plan, id=id, user=request.user)
            obj.is_done = True
            obj.save()
            return self.success_response(
                data=PlanSerializer(obj).data,
                message='malumot yangilandi'
            )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')