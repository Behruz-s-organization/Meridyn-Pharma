# rest framework 
from rest_framework import generics, permissions

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import TourPlan
from core.apps.shared.serializers.tour_plan import TourPlanSerializer
from core.apps.shared.serializers.base import BaseResponseSerializer, SuccessResponseSerializer
from core.apps.shared.utils.response_mixin import ResponseMixin



class TourPlanListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()
    permission_classes = [permissions.IsAuthenticated]

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