from azbankgateways.urls import az_bank_gateways_urls
from django.urls import path
from payment.views import go_to_gateway_view,callback_gateway_view,SendData

urlpatterns=[
        path("payment/" , SendData.as_view()),
        path('bankgateways/', az_bank_gateways_urls()),
        path("go-to-gateway/",go_to_gateway_view),
        path("callback-gateway/",callback_gateway_view),
]