from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from . import models
from .forms import ExpenseForm


def expense_list(request):
    categories = models.Category.objects.order_by("name")
    expenses = models.Expense.objects.select_related("category").order_by("-date", "-pk")
    selected_category = request.GET.get("category", "")

    if selected_category:
        expenses = expenses.filter(category_id=selected_category)

    total = expenses.aggregate(total=Sum("amount"))["total"] or 0
    return render(
        request,
        "expenses/expense_list.html",
        {
            "expenses": expenses,
            "categories": categories,
            "selected_category": selected_category,
            "total": total,
            "expense_count": expenses.count(),
        },
    )


def expense_detail(request, pk):
    expense = get_object_or_404(
        models.Expense.objects.select_related("category"), pk=pk
    )
    return render(request, "expenses/expense_detail.html", {"expense": expense})


def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(
        request,
        "expenses/expense_form.html",
        {"form": form, "page_title": "Add expense", "submit_label": "Save expense"},
    )


def expense_update(request, pk):
    expense = get_object_or_404(models.Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_detail", pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request,
        "expenses/expense_form.html",
        {"form": form, "page_title": "Edit expense", "submit_label": "Save changes"},
    )


def expense_delete(request, pk):
    expense = get_object_or_404(models.Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")
    return render(request, "expenses/expense_confirm_delete.html", {"expense": expense})
