from django.urls import path
from .views import (
    shopping_list_view,
    inventory_add,
    inventory_update,
    shopping_add,
    shopping_update,
    InventoryDelete,
    ShoppingDelete,
    inventory_move,
    shopping_move,
)

urlpatterns = [
    path("inventory/add", inventory_add, name="inventory_add"),
    path("inventory/<uuid:pk>/", inventory_update, name="inventory_update"),
    path(
        "inventory/delete/<uuid:pk>", InventoryDelete.as_view(), name="inventory_delete"
    ),
    path("inventory/move/<uuid:pk>", inventory_move, name="inventory_move"),
    path("shopping_list/", shopping_list_view, name="shopping_list"),
    path("shopping_list/add", shopping_add, name="shopping_add"),
    path("shopping_list/<uuid:pk>", shopping_update, name="shopping_update"),
    path(
        "shopping_list/delete/<uuid:pk>",
        ShoppingDelete.as_view(),
        name="shopping_delete",
    ),
    path("shopping_list/move/<uuid:pk>", shopping_move, name="shopping_move"),
]
