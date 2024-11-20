from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from accounts.forms import CustomerForm
from accounts.models import Transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Transaction, Customer
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.utils import timezone
from accounts.models import *
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    else:
        user = request.user,
        query_user = request.GET.get('username')
        username_prefill = ""
        if request.user == query_user:
            messages.error(request, 'You are already logged in')
            return redirect('dashboard')

        else:
            username_prefill = request.GET.get('username_prefill')

        print(username_prefill)
        context = {
            'username_prefill': username_prefill
        }
        return render(request, 'login.html', context)
    # return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


def transaction_details(request, id):
    # Retrieve the transaction using the provided ID
    transaction = get_object_or_404(Transaction, id=id)

    # Pass the transaction object to the template
    context = {
        'transaction': transaction,
    }

    return render(request, 'transaction_details.html', context)


@login_required
def search(request):
    transaction_types = Transaction.TRANSACTION_TYPES
    context = {
        'transaction_types': transaction_types
    }
    return render(request, 'search.html', context)


@login_required
def search_results(request):
    customer = request.GET.get('customer', '')
    salesperson = request.GET.get('salesperson', '')
    type = request.GET.get('type', '')
    description = request.GET.get('description', '')
    date = request.GET.get('date')

    transactions = Transaction.objects.all()

    if customer:
        transactions = transactions.filter(customer__name__icontains=customer)
    if salesperson:
        transactions = transactions.filter(
            salesperson__name__icontains=salesperson)
    if type:
        transactions = transactions.filter(type__iexact=type)
    if description:
        transactions = transactions.filter(description__icontains=description)
    if date:
        transactions = transactions.filter(date_time__date=date)
    transaction_types = Transaction.TRANSACTION_TYPES

    context = {
        'transactions': transactions,
        'customer': customer,
        'salesperson': salesperson,
        'type': type,
        'description': description,
        'date': date,
        'transaction_types': transaction_types
    }

    return render(request, 'search_results.html', context)


@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.delete()
    messages.success(request, 'Transaction deleted successfully')
    return redirect('dashboard')


@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        customer = request.POST.get('customer')
        if customer:
            customer_obj, created = Customer.objects.get_or_create(
                name=customer)
            transaction.customer = customer_obj

        transaction.amount = request.POST.get('amount')
        transaction.type = request.POST.get('type')
        transaction.description = request.POST.get('description')
        transaction.edited_by = request.user
        transaction.edited_on = datetime.now()
        transaction.save()
        messages.success(request, 'Transaction updated successfully')
        return redirect('dashboard')
    else:
        print(transaction)
        return render(request, 'edit_transaction.html', {'transaction': transaction})


# List Customers
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_on')
    return render(request, 'customer_list.html', {'customers': customers})

# Add Customer


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

# Edit Customer


@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

# Delete Customer


@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')
    return render(request, 'delete_customer.html', {'customer': customer})


@login_required
def customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    transactions = customer.transaction_set.all().order_by('-date_time')
    total_transactions = transactions.count()
    total_spent = transactions.filter(type='sale').aggregate(
        Sum('amount'))['amount__sum'] or 0
    total_credit = transactions.filter(type='credit').aggregate(Sum('amount'))[
        'amount__sum'] or 0

    context = {
        'customer': customer,
        'transactions': transactions,
        'total_transactions': total_transactions,
        'total_spent': total_spent,
        'total_credit': total_credit,
    }
    return render(request, 'customer_details.html', context)


@login_required(login_url='/login/')
def transactions_page(request):
    # Get all transactions
    transactions = Transaction.objects.all().order_by('-date_time')

    # Filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transaction_type = request.GET.get('type')
    customer_id = request.GET.get('customer')
    salesperson_id = request.GET.get('salesperson')

    # Apply filters
    if start_date:
        transactions = transactions.filter(date_time__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date_time__date__lte=end_date)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    if customer_id:
        transactions = transactions.filter(customer_id=customer_id)
    if salesperson_id:
        transactions = transactions.filter(salesperson_id=salesperson_id)

    # Aggregates
    total_income = transactions.filter(type='sale').aggregate(Sum('amount'))[
        'amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))[
        'amount__sum'] or 0
    total_credit = transactions.filter(type='credit').aggregate(Sum('amount'))[
        'amount__sum'] or 0

    # Pagination
    paginator = Paginator(transactions, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get choices for filters
    transaction_types = Transaction.TRANSACTION_TYPES
    customers = Customer.objects.all()
    salespersons = User.objects.all()

    context = {
        'page_obj': page_obj,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_credit': total_credit,
        'transaction_types': transaction_types,
        'customers': customers,
        'salespersons': salespersons,
    }
    return render(request, 'transactions_page.html', context)
