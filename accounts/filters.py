import django_filters
from .models import *
from django_filters import DateFilter, CharFilter, DateRangeFilter, DateFromToRangeFilter


# class OrderFilter(django_filters.FilterSet):
# 	start_date  = DateFilter(field_name='date_created', lookup_expr='gte')
# 	end_date 	= DateFilter(field_name='date_created', lookup_expr='lte')
# 	note 		= CharFilter(field_name='note', lookup_expr='icontains')

# 	class Meta:
# 		model 	= Order
# 		fields	= '__all__'
# 		exclude = ['customer', 'date_created']


# class DepositFilter(django_filters.FilterSet):
# 	start_date  = DateFilter(field_name='date_created', lookup_expr='gt', label='Start Date(01/01/2021)')
# 	end_date 	= DateFilter(field_name='date_created', lookup_expr='lt', label='End Date(12/31/2021)')
# 	date_range 	= DateRangeFilter(field_name='date')
# 	note 		= CharFilter(field_name='remark', lookup_expr='icontains', label='Remark')

# 	class Meta:
# 		model 	= Transaction
# 		fields	= ['bank', 'game_backend', 'admin', 'promotion',]


class DepositFilter(django_filters.FilterSet):
	date 		= DateFromToRangeFilter(field_name='date_created')
	#end_date 	= DateFilter(field_name='date_created', lookup_type='lte', label='End Date(12/31/2021)')
	date_value 	= DateFilter(field_name='date')
	note 		= CharFilter(field_name='remark', lookup_expr='icontains', label='Remark')
	game 		= CharFilter(field_name='game__game_name__name', lookup_expr='icontains', label='Game')
	bank		= CharFilter(field_name='bank__bank_name', lookup_expr='icontains', label='Bank')
	admin		= CharFilter(field_name='admin', lookup_expr='icontains', label='Admin')
	promotion	= CharFilter(field_name='promotion__name', lookup_expr='icontains', label='Promotion')
	remark		= CharFilter(field_name='remark', lookup_expr='icontains', label='Remark')

	class Meta:
		model 	= Transaction
		fields	= ['game', 'bank', 'admin', 'game_backend', 'promotion', 'date', 'date_value']
	

