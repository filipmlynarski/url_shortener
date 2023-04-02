from rest_framework.generics import CreateAPIView, RetrieveAPIView

from alias.models import Alias
from alias.serializers import AliasCreateSerializer, AliasDetailSerializer


class AliasCreateView(CreateAPIView):
    serializer_class = AliasCreateSerializer


class AliasDetailView(RetrieveAPIView):
    queryset = Alias.objects.all()
    lookup_field = 'alias'
    serializer_class = AliasDetailSerializer
