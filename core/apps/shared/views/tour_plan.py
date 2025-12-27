# django
from django.shortcuts import get_object_or_404

# rest framework 
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import TourPlan
from core.apps.shared.serializers.tour_plan import TourPlanSerializer, TourPlanUpdateSerializer, TourPlanCreateSerializer
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin



class TourPlanListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    
    @swagger_auto_schema(
        responses={
            200: SuccessResponseSerializer(),
            400: BaseResponseSerializer(),
            500: BaseResponseSerializer(),
        }
    )
    def get(self, request):
        try:
            queryset = self.queryset.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(data=serializer.data, message='malumot fetch qilindi') 
        except Exception as e:
            return self.error_response(data=str(e), message='xatolik')
        

class TourPlanUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = TourPlanUpdateSerializer
    queryset = TourPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        obj = get_object_or_404(TourPlan, id=id, user=request.user)
        serializer = self.serializer_class(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                data={},
                message="tahrirlandi"
            )
        return self.failure_response(data=serializer.errors, message='xato')
    

class TourPlanCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = TourPlanCreateSerializer
    queryset = TourPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                tour_plan = serializer.save()
                return self.success_response(
                    data=TourPlanSerializer(tour_plan).data,
                    message="Tour plan created successfully",
                )
            return self.failure_response(
                data=serializer.errors,
                message="Failed when tour plan create process"
            )
        except Exception as e:
            return self.error_response(
                data=str(e)
            )
        