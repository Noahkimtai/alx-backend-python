import django_filters
from django.db.models import Q
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Enable filtering data by date range, search text and participants
    """

    # filter by sender ID

    sender_name = django_filters.CharFilter(method="sednder_filter")

    def sednder_filter(self, queryset, name, value):
        return queryset.filter(
            Q(sender__first_name__icontains=value)
            | Q(sender__last_name__icontains=value)
        )

    # Date range filters
    start_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    # Filter by search text
    search = django_filters.CharFilter(
        field_name="message_body", lookup_expr="icontains"
    )

    class Meta:
        model = Message
        fields = "__all__"
