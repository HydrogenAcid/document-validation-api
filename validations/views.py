
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

from .filters import QTextSearchFilter
from .models import Validation
from .serializers import ValidationCreateSerializer,ValidationDetailSerializer
from .permissions import IsOwner
from .pagination import PageLimitPagination

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
        