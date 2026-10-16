from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
class Expense(models.Model):
    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    date=models.DateField()

    def __str__(self):
        return self.title
