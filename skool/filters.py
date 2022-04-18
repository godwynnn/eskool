from attr import fields
import django_filters
from .models import *


class ResultFilter(django_filters.FilterSet):
    
    class Meta:
        model= Result
        fields=['level','term','course']