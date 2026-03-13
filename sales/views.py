from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import SaleForm
from .models import Sale
from inventory.models import Product

def pos(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)

            product = sale.product
            quantity = sale.quantity_sold

            sale.total_price = product.price * quantity

            # reduce stock
            product.quantity -= quantity
            product.save()

            sale.save()

            return redirect('pos')

    else:
        form = SaleForm()

    sales = Sale.objects.all().order_by('-sold_at')[:10]

    return render(request, 'sales/pos.html', {
        'form': form,
        'sales': sales
    })