from drf_yasg import openapi

lat_param = openapi.Parameter(
    'lat', openapi.IN_QUERY,
    description="Query param lat", type=openapi.TYPE_NUMBER
)
long_param = openapi.Parameter(
    'long', openapi.IN_QUERY,
    description="Query param long", type=openapi.TYPE_NUMBER
)

filial_extra_params = [lat_param, long_param]
