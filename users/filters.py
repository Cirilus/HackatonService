
from .models import Feedback

import django_filters





class FeedbackFilter(django_filters.FilterSet):
    create_at = django_filters.DateFilter(lookup_expr='date__exact')
    create_at__gt = django_filters.DateFilter(field_name='create_at', lookup_expr='gt')
    create_at__lt = django_filters.DateFilter(field_name='create_at', lookup_expr='lt')


    class Meta:
        model = Feedback
        fields = ['create_at', 'status' ]