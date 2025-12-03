# django
from django.shortcuts import get_object_or_404
# rest framework 
from rest_framework import generics, permissions, views

# drf yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# shared
from core.apps.shared.models import Plan
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
from core.apps.shared.serializers.plan import PlanSerializer, PlanUpdateSerializer, PlanCreateSerializer, PlanCompliteSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin



class PlanApiView(generics.GenericAPIView, ResponseMixin):
    queryset = Plan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlanCreateSerializer
        else:
            return PlanSerializer

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
            serializer = self.get_serializer(queryset, many=True)
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
            serializer = self.get_serializer(data=request.data, context={'user': request.user})
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
    serializer_class = PlanCompliteSerializer
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
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                comment = serializer.validated_data.get('comment')
                obj.is_done = True
                obj.comment = comment
                obj.save()
                return self.success_response(
                    data=PlanSerializer(obj).data,
                    message='malumot yangilandi'
                )
            else:
                return self.failure_response(
                    data=serializer.errors,
                    message="malumot yangilanmadi"
                )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        

class PlanUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PlanUpdateSerializer
    queryset = Plan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "malumot tahrirlandi",
                        "data": {
                            "id": 1,
                            "title": "string",
                            "description": "string",
                            "date": "string",
                            "is_done": "true",
                            "created_at": "string",
                        }
                    }
                }
            ),
            400: openapi.Response(
                schema=None,
                description="Failure",
                examples={
                    "application/json": {
                        "status_code": 400,
                        "status": "failure",
                        "message": "malumot tahrirlanmadi",
                        "data": "string"
                    }
                }
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="Not Found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "status": "failure",
                        "message": "Plan topilmadi",
                        "data": {}
                    }
                }
            )
        }
    )
    def patch(self, request, id):
        try:
            obj = Plan.objects.filter(id=id, user=request.user).first()
            if not obj:
                return self.failure_response(message="Plan topilmadi", data={}, status_code=404)
            serializer = self.serializer_class(data=request.data, instance=obj)
            if serializer.is_valid():
                obj = serializer.save()
                created_data = PlanSerializer(obj).data
                return self.success_response(
                    data=created_data, 
                    message='malumot tahrirlandi', 
                    status_code=200
                )
            return self.failure_response(data=serializer.errors, message='malumot tahrirlanmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        


class PlanDeleteApiView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                schema=None,
                description="Success",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "status": "success",
                        "message": "Plan o'chirildi",
                        "data": {}
                    }
                }
            ),
            500: openapi.Response(
                schema=None,
                description="Server Error",
                examples={
                    "application/json": {
                        "status_code": 500,
                        "status": "error",
                        "message": "xatolik",
                        "data": "string"
                    }
                }
            ),
            404: openapi.Response(
                schema=None,
                description="Not Found",
                examples={
                    "application/json": {
                        "status_code": 404,
                        "status": "failure",
                        "message": "Plan topilmadi",
                        "data": {}
                    }
                }
            )
        }
    )
    def delete(self, request, id):
        try:
            obj = Plan.objects.filter(id=id, user=request.user).first()
            if not obj:
                return self.failure_response(message="Plan topilmadi", status_code=404, data={})
            obj.delete()
            return self.success_response(message="Plan o'chirildi", status_code=204, data={})
        except Exception as e:
            return self.error_response(data=str(e), message="xatolik")