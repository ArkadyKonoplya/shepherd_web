from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib import messages

from .models import Inventory, ShoppingList
from .forms import InventoryForm, ShoppingListForm
from farm.models import Farm

@login_required
def shopping_list_view(request):
    shopping_list = ShoppingList.objects.select_related("unit_of_measure").filter(
        farm_id__member_farms__user_id=request.user.id
    )

    inventory = Inventory.objects.select_related("unit_of_measure").filter(
        farm_id__member_farms__user_id=request.user.id
    )

    return render(
        request,
        "inventory/inventory.html",
        {"shopping_list": shopping_list, "inventory": inventory},
    )


@login_required
def inventory_add(request):

    form = InventoryForm(request.POST or None, user=request.user)

    if form.is_valid():
        farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

        item = form.save(commit=False)
        item.farm_id = farm
        item.save()

        messages.add_message(request, messages.SUCCESS, "Inventory item added.")

        return redirect("inventory")

    return render(
        request, "inventory/inventory_form.html", {"form": form, "type": "inventory"}
    )


@login_required
def inventory_move(request, pk):

    item = get_object_or_404(Inventory, pk=pk)
    farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

    if request.POST and item.farm_id == farm:
        shopping_item = ShoppingList()
        shopping_item.item = item.item
        shopping_item.quantity = item.quantity
        shopping_item.farm_id = item.farm_id
        shopping_item.unit_of_measure = item.unit_of_measure
        shopping_item.location = item.location
        shopping_item.save()

        item.delete()

        return redirect("inventory")

    return render(
        request, "inventory/inventory_move.html", {"item": item, "type": "Shopping"}
    )


@login_required
def inventory_update(request, pk):

    item = get_object_or_404(Inventory, pk=pk)

    form = InventoryForm(request.POST or None, instance=item, user=request.user)

    if form.is_valid():
        farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

        item = form.save(commit=False)
        item.farm_id = farm
        item.save()

        return redirect("inventory")

    return render(
        request, "inventory/inventory_form.html", {"form": form, "type": "inventory"}
    )


class InventoryDelete(DeleteView):
    model = Inventory
    success_url = "/inventory/inventory/"
    template_name = "inventory/inventory_delete.html"


@login_required
def shopping_add(request):

    form = ShoppingListForm(request.POST or None, user=request.user)

    if form.is_valid():
        farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

        item = form.save(commit=False)
        item.farm_id = farm
        item.save()
        messages.add_message(request, messages.SUCCESS, "Shopping item added.")

        return redirect("shopping_list")

    return render(
        request,
        "inventory/inventory_form.html",
        {"form": form, "type": "shopping_list"},
    )


@login_required
def shopping_move(request, pk):

    item = get_object_or_404(ShoppingList, pk=pk)
    farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

    if request.POST and item.farm_id == farm:
        inventory_item = Inventory()
        inventory_item.item = item.item
        inventory_item.quantity = item.quantity
        inventory_item.farm_id = item.farm_id
        inventory_item.unit_of_measure = item.unit_of_measure
        inventory_item.location = item.location
        inventory_item.save()

        item.delete()

        return redirect("shopping_list")

    return render(
        request, "inventory/inventory_move.html", {"item": item, "type": "Inventory"}
    )


@login_required
def shopping_update(request, pk):

    item = get_object_or_404(ShoppingList, pk=pk)

    form = ShoppingListForm(request.POST or None, instance=item, user=request.user)

    if form.is_valid():
        farm = Farm.objects.get(member_farms__user_id=request.user, member_farms__default_farm=True)

        item = form.save(commit=False)
        item.farm_id = farm
        item.save()

        return redirect("shopping_list")

    return render(request, "inventory/inventory_form.html", {"form": form})


class ShoppingDelete(DeleteView):
    model = ShoppingList
    success_url = "/inventory/shopping_list/"
    template_name = "inventory/inventory_delete.html"
