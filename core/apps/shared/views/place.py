# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Place
from core.apps.shared.serializers import base as base_serializer
from core.apps.shared.serializers.place import PlaceSerializer, PlaceCreateSerializer, PlaceUpdateSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin

# accounts
from core.apps.accounts.models import User


class PlaceListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: base_serializer.SuccessResponseSerializer(),
            400: base_serializer.BaseResponseSerializer(),
            500: base_serializer.BaseResponseSerializer(),
        },
    )
    def get(self, request):
        try:
            search = request.query_params.get('search')

            query = self.queryset.filter(user=request.user)
            if search:
                query = query.filter(name__istartswith=search)

            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.success_response(data=self.paginate_queryset(serializer.data), message='malumotlar fetch qilindi')

            serializer = self.serializer_class(query, many=True)
            return self.success_response(data=serializer.data, message='malumotlar fetch qilindi')

        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        

class PlaceCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PlaceCreateSerializer
    queryset = Place.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            201: base_serializer.SuccessResponseSerializer(),
            400: base_serializer.BaseResponseSerializer(),
            500: base_serializer.BaseResponseSerializer()
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                instance = serializer.save()
                return self.success_response(data=PlaceSerializer(instance).data, message='malumot qoshildi')
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        


class PlaceDeleteUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = PlaceUpdateSerializer
    queryset = Place.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: base_serializer.SuccessResponseSerializer(),
            400: base_serializer.BaseResponseSerializer(),
            500: base_serializer.BaseResponseSerializer(),
        }
    )
    def patch(self, request, id):
        try:
            obj = get_object_or_404(Place, id=id, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=obj)
            if serializer.is_valid():
                instance = serializer.save()
                return self.success_response(
                    data=PlaceSerializer(instance).data,
                    message='Malumot tahrilandi'
                )
            return self.failure_response(
                data=serializer.errors,
                message='Malumot tahrirlanmadi'
            )
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')

    
    @swagger_auto_schema(
        responses={
            204: base_serializer.SuccessResponseSerializer(),
            400: base_serializer.BaseResponseSerializer(),
            500: base_serializer.BaseResponseSerializer(),
        }
    )
    def delete(self, request, id):
        try:
            obj = get_object_or_404(Place, id=id, user=request.user)
            obj.delete()
            return self.success_response(message='Malumot ochirildi', status_code=204)
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
