from django.urls import path
from django.views.generic import TemplateView

from .views import (
    HistorySetterAjaxView,
    HistoryView,
    HomePageView,
    OrderView,
    PriceSetterAjaxView,
    TotalAmountCounterAjaxView,
)

app_name = "smakolyk"

urlpatterns = [
    path("", TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    path("smakolyk/", HomePageView.as_view(), name="home"),
    path("create-order/", OrderView.as_view(), name="order"),
    path(
        "order-error/",
        TemplateView.as_view(template_name="order_error.html"),
        name="order_error",
    ),
    path(
        "success-order/",
        TemplateView.as_view(template_name="order_success.html"),
        name="order_success",
    ),
    path("set-price/", PriceSetterAjaxView.as_view(), name="set_price"),
    path(
        "set-total-price/", TotalAmountCounterAjaxView.as_view(), name="set_total_price"
    ),
    path("history/", HistoryView.as_view(), name="history"),
    path("get-history-week/", HistorySetterAjaxView.as_view(), name="get_history_week"),
    path(
        "order-access-denied/",
        TemplateView.as_view(template_name="access_denied_order.html"),
        name="weekend",
    ),
]
