import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Products, Category, CartItem
from .forms import SearchForm

# Constants
now = datetime.datetime.now()
date_str = now.strftime("%d-%m-%Y")



def search(request):
    form = SearchForm(request.GET)
    products = Products.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        # Q obyektlari orqali bir nechta shartni birlashtiramiz
        products = products.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
        )

    return render(request, 'app_main/main.html', {'page_obj': form, 'page_obj': products})


# Views for displaying products and categories
def product_list(request):
    products = Products.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "app_main/main.html", {"page_obj": page_obj})


def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "app_main/category.html", {"page_obj": page_obj})


def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Products.objects.filter(category=category)
    paginator = Paginator(products, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "app_main/product_list.html", {"category": category, "page_obj": page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'app_main/product-detail.html', {'product': product})


# Cart Views (Login required)
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    finaly_total_amount = total_amount + 10
    shipping_date = now + datetime.timedelta(days=10)
    shipping_date = shipping_date.strftime("%d-%m-%Y")

    return render(request, 'app_main/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'finaly_total_amount': finaly_total_amount,
        'date_str': date_str,
        'shipping_date': shipping_date
    })



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    # Xabarni ko'rsatish
    messages.success(request, f"{product.title} savatga {quantity} dona qo'shildi!")

    # AJAX so'rovini tekshirish
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # Agar bu AJAX so'rovi bo'lsa
        return JsonResponse({'message': f"{product.title} savatga {quantity} dona qo'shildi!"})

    # Oddiy so'rov bo'lsa, sahifa qayta yuklanadi
    return HttpResponse(status=204)  # Faqat xabarni ko'rsatadi, sahifani qayta yuklamaydi


@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')


@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item = CartItem.objects.get(product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')


# Checkout and email notification
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        total_amount = 0
        cart_details = []

        for item in cart_items:
            total_amount += item.total_price
            cart_details.append({
                'title': item.product.title,
                'quantity': item.quantity,
                'price': item.product.new_price,
                'total_price': item.total_price,
                'image_url': item.product.image.url,
                'delivery_date': '2024-12-01',
            })
        
        email_content = "<h3>Your Order Details</h3>"
        email_content += f"<p>Total Amount: ${total_amount}</p>"
        
        for item in cart_details:
            email_content += f"""
            <p><strong>{item['title']}</strong></p>
            <p>Price: ${item['price']}</p>
            <p>Quantity: {item['quantity']}</p>
            <p>Total Price: ${item['total_price']}</p>
            <p><img src="{item['image_url']}" alt="{item['title']}"></p>
            <p>Expected Delivery: {item['delivery_date']}</p>
            <hr>
            """
        
        send_mail(
            'Your Order Details',
            '',  # No plain text body
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
            html_message=email_content,
        )

        return HttpResponse("Checkout successful! An email has been sent.")

    return render(request, 'checkout.html')
