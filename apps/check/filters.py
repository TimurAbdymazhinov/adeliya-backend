import django_filters

from apps.check.models import Check


class CheckFilter(django_filters.FilterSet):
    start_date = django_filters.CharFilter(
        field_name='accrued_point_date', method='start_date_filter'
    )
    end_date = django_filters.CharFilter(
        field_name='accrued_point_date', method='end_date_filter'
    )

    class Meta:
        model = Check
        fields = ['start_date', 'end_date']

    def start_date_filter(self, queryset, name, value):
        if 'end_date' in self.request.GET:
            return queryset.filter(accrued_point_date__date__gte=value)
        return queryset.filter(accrued_point_date__date=value)

    def end_date_filter(self, queryset, name, value):
        self.end_date = value
        return queryset.filter(accrued_point_date__date__lte=value)
