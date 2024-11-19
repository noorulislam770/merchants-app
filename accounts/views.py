from django.shortcuts import redirect, render
from .models import Transaction, Customer
from .forms import TransactionForm, CustomerForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login/')
def dashboard(request):
    transaction = Transaction.objects.all().order_by('-date_time')
    paginator = Paginator(transaction, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_income = sum(t.amount for t in transaction if t.type == 'sale')
    total_expense = sum(t.amount for t in transaction if t.type == 'expense')
    total_credit = sum(t.amount for t in transaction if t.type == 'credit')

    context = {
        # 'transactions': transaction,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_credit': total_credit,
    }

    transaction_types = Transaction.TRANSACTION_TYPES
    context['transaction_types'] = transaction_types
    context['page_obj'] = page_obj

    return render(request, 'dashboard.html', context)


def add_transaction(request):
    if (request.method == 'POST'):
        if (request.POST.get('customer') and request.POST.get('amount') and request.POST.get('type') and request.POST.get('description')):
            cusotmer_name = request.POST.get('customer')
            customer, created = Customer.objects.get_or_create(
                name=cusotmer_name)

            amount = request.POST.get('amount')
            type = request.POST.get('type')
            description = request.POST.get('description')
            salesperson = request.user

            transaction = Transaction.objects.create(
                customer=customer,
                amount=float(amount),
                type=type,
                description=description,
                salesperson=salesperson
            )
            transaction.save()
            messages.success(request, 'Transaction added successfully')
            return redirect(dashboard)

        else:
            # form = TransactionForm()
            messages.error(request, 'Transaction not added, invalid form data')
            return render(request, 'dashboard.html',)

    else:
        return redirect(dashboard)
