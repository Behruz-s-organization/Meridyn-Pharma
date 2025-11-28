# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework import generics, permissions, views

# shared
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.region import RegionSerializer
from core.apps.shared.models import Region


class RegionListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    def get(self, request):
        try:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return self.success_response(
                data=serializer.data, message='malumotlar fetch qilindi'
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
        

class RegionCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        try:   
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                region = Region.objects.create(name=name)
                return self.success_response(data=RegionSerializer(region).data, message='malumot qoshildi')
            return self.failure_response(data=serializer.errors, message='malumot qoshilmadi')

        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
        


class RegionUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, id):
        try:   
            obj = get_object_or_404(Region, id=id)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                obj.name = name
                obj.save()
                return self.success_response(data=RegionSerializer(obj).data, message='malumot tahrirlandi')
            return self.failure_response(data=serializer.errors, message='malumot tahrirlanmadi')

        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
        


class RegionDeleteApiView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, id):
        try:   
            obj = get_object_or_404(Region, id=id)
            obj.delete()       
            return self.success_response(data={}, message='malumot ochirildi')

        except Exception as e:
            return self.error_response(
                data=str(e),
                message="xatolik"
            )
        
