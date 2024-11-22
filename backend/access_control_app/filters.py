from django_filters import rest_framework as filters
from .models import RegistroAcesso
from django.db.models import Q

class RegistroAcessoFilter(filters.FilterSet):
    data = filters.DateFilter(method='filter_by_date')

    class Meta:
        model = RegistroAcesso
        fields = []

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(
            Q(data_hora_entrada__date=value) | Q(data_hora_saida__date=value)
        )
