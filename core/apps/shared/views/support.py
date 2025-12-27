# rest framework
from rest_framework import generics, permissions

# drf yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# shared
from core.apps.shared.models import Support
from core.apps.shared.utils.response_mixin import ResponseMixin
from core.apps.shared.serializers.support import SupportCreateSerializer, SupportListSerializer


class SupportCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = SupportCreateSerializer
    queryset = Support.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={"user": request.user})
            if serializer.is_valid():
                data = serializer.save()
                return self.success_response(
                    data={},
                    message="Xabar yuborildi",
                    status_code=201
                )
            return self.failure_response(
                data=serializer.errors,
                message='Xabar yuborilmadi, iltimos malumotlar togri ekanligini tekshirib koring',
            )
        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik, backend dastruchiga murojaat qiling iltimos'
            )


class SupportListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = SupportListSerializer
    queryset = Support.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="problem",
                description="problem text bo'yicha filter",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="district",
                description="tuman name bo'yicha filter",
                required=False,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                in_=openapi.IN_QUERY,
                name="date",
                description="date bo'yicha qidirish",
                required=False,
                type=openapi.FORMAT_DATE,
            ),
        ],
    )
    def get(self, request):
        try:
            problem = request.query_params.get('problem', None)
            district_name = request.query_params.get('district', None)
            date = request.query_params.get('date', None)
            
            queryset = self.queryset.filter(user=request.user)

            # filters
            if problem is not None:
                queryset = queryset.filter(problem__istartswith=problem)
            
            if district_name is not None:
                queryset = queryset.filter(district__name__istartswith=district_name)

            if date is not None:
                queryset = queryset.filter(date=date)

            serializer = self.serializer_class(queryset, many=True)
            return self.success_response(
                data=serializer.data,
                message='Malumotlar fetch qilindi'
            )

        except Exception as e:
            return self.error_response(
                data=str(e),
                message='xatolik, iltimos backend dasturchiga murojaat qiling'
            )