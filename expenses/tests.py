from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Expense


class ExpenseViewsTests(TestCase):
    def setUp(self):
        self.food = Category.objects.create(name="Food")
        self.travel = Category.objects.create(name="Travel")
        self.lunch = Expense.objects.create(
            title="Lunch", amount=Decimal("12.50"), category=self.food, date=date(2026, 10, 1)
        )
        self.train = Expense.objects.create(
            title="Train", amount=Decimal("8.00"), category=self.travel, date=date(2026, 10, 2)
        )

    def test_expense_list_shows_total_and_category_filter(self):
        response = self.client.get(reverse("expense_list"), {"category": self.food.pk})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lunch")
        self.assertNotContains(response, "Train")
        self.assertEqual(response.context["total"], Decimal("12.50"))
        self.assertEqual(response.context["expense_count"], 1)

    def test_expense_list_shows_all_expenses_without_filter(self):
        response = self.client.get(reverse("expense_list"))

        self.assertContains(response, "Lunch")
        self.assertContains(response, "Train")
        self.assertEqual(response.context["total"], Decimal("20.50"))

    def test_create_expense(self):
        response = self.client.post(
            reverse("expense_create"),
            {
                "title": "Coffee",
                "amount": "3.25",
                "category": self.food.pk,
                "date": "2026-10-03",
            },
        )

        self.assertRedirects(response, reverse("expense_list"))
        self.assertTrue(Expense.objects.filter(title="Coffee").exists())

    def test_invalid_create_keeps_form_errors_visible(self):
        response = self.client.post(
            reverse("expense_create"),
            {"title": "", "amount": "3.25", "category": self.food.pk, "date": "2026-10-03"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_update_expense(self):
        response = self.client.post(
            reverse("expense_update", args=[self.lunch.pk]),
            {
                "title": "Team lunch",
                "amount": "18.00",
                "category": self.travel.pk,
                "date": "2026-10-04",
            },
        )

        self.assertRedirects(response, reverse("expense_detail", args=[self.lunch.pk]))
        self.lunch.refresh_from_db()
        self.assertEqual(self.lunch.title, "Team lunch")
        self.assertEqual(self.lunch.amount, Decimal("18.00"))
        self.assertEqual(self.lunch.category, self.travel)

    def test_delete_requires_post_confirmation(self):
        response = self.client.get(reverse("expense_delete", args=[self.lunch.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This action can't be undone.")
        self.assertTrue(Expense.objects.filter(pk=self.lunch.pk).exists())

        response = self.client.post(reverse("expense_delete", args=[self.lunch.pk]))

        self.assertRedirects(response, reverse("expense_list"))
        self.assertFalse(Expense.objects.filter(pk=self.lunch.pk).exists())
