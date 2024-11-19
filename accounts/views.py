from django.shortcuts import redirect, render
from .models import Transaction, Customer
from .forms import TransactionForm, CustomerForm

# Create your views here.


def dashboard(request):
    transaction = Transaction.objects.all()
    total_income = sum(t.amount for t in transaction if t.type == 'sale')
    total_expense = sum(t.amount for t in transaction if t.type == 'expense')
    total_credit = sum(t.amount for t in transaction if t.type == 'credit')

    context = {
        'transactions': transaction,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_credit': total_credit,
    }

    return render(request, 'dashboard.html', context)


def add_transaction(request):
    if (request.method == 'POST'):
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            form = TransactionForm()
        return render(request, 'add_transaction.html', {'form': form})
