import json
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Transaction
from django.contrib.auth.decorators import login_required, user_passes_test

# Only staff users can access POS
def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
def pos(request):
    products = Product.objects.all()
    return render(request, "sales/pos.html", {"products": products})

@login_required
@user_passes_test(staff_required)
def cart_view(request):
    cart = request.session.get("cart", {})
    total = sum(item["total"] for item in cart.values())
    return render(request, "sales/cart.html", {"cart": cart, "total": total})

@login_required
@user_passes_test(staff_required)
@csrf_exempt
def checkout(request):
    if request.method == "POST":
        # Get cart data from JS
        cart_data = json.loads(request.POST.get("cart_data", "{}"))
        total = sum(item["total"] for item in cart_data.values())

        # Save transaction
        transaction = Transaction.objects.create(total=total, cashier=request.user)

        # Reduce stock
        for pid, item in cart_data.items():
            product = Product.objects.get(id=pid)
            product.stock -= item["qty"]
            product.save()

        # Clear session cart
        request.session["cart"] = {}

        # Show receipt
        return render(request, "sales/receipt.html", {"cart": cart_data, "total": total, "transaction": transaction})

    return redirect("pos")

# Optional: view past receipts
@login_required
@user_passes_test(staff_required)
def receipt(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    # For simplicity, we just show total; for itemized, add TransactionItem model
    return render(request, "sales/receipt.html", {"cart": {}, "total": transaction.total, "transaction": transaction})

@login_required
@user_passes_test(staff_required)
def products(request):
    products = Product.objects.all()
    return render(request, "sales/products.html", {"products": products})

@login_required
@user_passes_test(staff_required)
def dashboard(request):
    total_products = Product.objects.count()
    today = timezone.now().date()
    sales_today = Transaction.objects.filter(date__date=today)
    total_sales = sum(t.total for t in sales_today)
    low_stock_count = Product.objects.filter(stock__lte=10).count()
    recent_transactions = Transaction.objects.order_by("-date")[:5]

    context = {
        "total_products": total_products,
        "total_sales": total_sales,
        "low_stock_count": low_stock_count,
        "recent_transactions": recent_transactions,
    }
    return render(request, "sales/dashboard.html", context)