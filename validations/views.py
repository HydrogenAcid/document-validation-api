
from rest_framework import viewsets,mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Validation
from .serializers import ValidationCreateSerializer,ValidationDetailSerializer,ValidationUploadSerializer
from .permissions import IsOwner
from .pagination import PageLimitPagination
from .filters import QTextSearchFilter

from .extractor import extract_rfc_from_xlsx
from .errors import api_error

class ValidationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    
):
    permission_classes = [IsAuthenticated]
    filter_backends = [QTextSearchFilter]
    search_fields = ['title']
    
    pagination_class = PageLimitPagination

    def get_queryset(self):
        if getattr(self,"swagger_fake_view",False):
            return Validation.objects.none()
        return Validation.objects.filter(created_by=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ValidationCreateSerializer
        return ValidationDetailSerializer
    
    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()
    @extend_schema(
    request=ValidationUploadSerializer,
    responses={
        200: OpenApiResponse(description="File processed"),
        400: OpenApiResponse(description="Validation error"),
        413: OpenApiResponse(description="File Too Large"),
    },
    description="Upload an XLSX file to extract RFC. Updates the Validation with status and extracted fields.",
)
    @action(detail=True, methods=['post'], url_path="file",parser_classes=[MultiPartParser])
    def upload_file(self, request, pk=None):

        """
        Upload an XLSX file and Extract RFC.
        Updates the Validation with status/extracted fields.
        """
        validation =self.get_object() # ownership via queryset + IsOwner in retrieve; queryset already filters

        f = request.FILES.get('file')
        if not f:
            return api_error("FILE_MISSING","File is required")
        
        #Basic type check extension
        if not f.name.lower().endswith('.xlsx'):
            return api_error("FILE_INVALID","Only .xlsx files are supported")
        
        # Size limit (expample: 5MB)
        max_bytes = 5 * 1024 * 1024
        if f.size and f.size > max_bytes:
            return api_error("FILE_TOO_LARGE","File too large",{"max_bytes":max_bytes},status_code=413)
        
        #Extract RFC
        try:
            rfc = extract_rfc_from_xlsx(f)
        except Exception as e:
            validation.status = "ERROR"
            validation.extracted_key ="RFC"
            validation.extracted_value = None
            validation.save(update_fields=["status","extracted_key","extracted_value"])
            return api_error("EXTRACTION_ERROR","Failed to proccess file",{"error":str(e)}, status_code=400)
        
        if not rfc:
            validation.status = "ERROR"
            validation.extracted_key="RFC"
            validation.extracted_value = None
            validation.save(update_fields=["status","extracted_key","extracted_value"])
            return api_error("KEY_NOT_FOUND","RFC not found in document", {"key":"RFC"}, status_code=400)
        
        validation.status = "PROCESSED"
        validation.extracted_key = "RFC"
        validation.extracted_value = rfc
        validation.save(update_fields=["status","extracted_key","extracted_value"])

        return Response(
            {
                "validation_id":str(validation.id),
                "status": validation.status,
                "extracted_key": validation.extracted_key,
                "extracted_value": validation.extracted_value,
            },
            status=status.HTTP_200_OK,
        )



        