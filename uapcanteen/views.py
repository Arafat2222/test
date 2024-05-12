from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings



# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        
        Contact.objects.create(name=name, email=email, phone=phone, message=message)

        
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')

    
    messages_info = messages.get_messages(request)
    return render(request, 'contact.html', {'messages': messages_info})

def getmessage(request):
    contact = Contact.objects.all()
    return render(request, 'message.html', {'contact': contact})    

def dashboard(request):
    return render(request, 'dashboard.html')

def trackorder(request):
    orders = Order.objects.all()
    return render(request, 'trackorder.html', {'orders': orders})

def update_order(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'completed':
            order.is_completed = True
        elif status == 'not_completed':
            order.is_completed = False
        elif status == 'cancelled':
            order.is_cancelled = True
        elif status == 'not_cancelled':
            order.is_cancelled = False
        elif status == 'delete':
            order.delete()
            return redirect('trackorder')    
        order.save()

    
    return redirect('trackorder')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'signup.html')

       
        user = User.objects.create_user(username=username, email=email, password=password)

        
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  
         
        else:
            
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    django_logout(request)
    return redirect('home')

@login_required
def userprofile(request):
  
    user = request.user
    
    
    orders = Order.objects.filter(user=user)

    
    return render(request, 'userprofile.html', {'user': user, 'orders': orders})


def ownerlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

     
        owner = Owner.objects.filter(username=username, password=password)
        if owner.exists():
            
            request.session['owner_username'] = username
            return redirect('dashboard')  
        else:
            
            messages.error(request, 'Invalid username or password.')
            return redirect('ownerlogin')
    return render(request, 'ownerlogin.html')

def ownerlogout(request):
    if 'owner_username' in request.session:
        del request.session['owner_username']
    return redirect('home')


# Views for displaying the menu items
def breakfast(request):
    breakfasts = Breakfast.objects.all()
    return render(request, 'breakfast.html', {'breakfasts': breakfasts})

def lunch(request):
    lunches = Lunch.objects.all()
    return render(request, 'lunch.html', {'lunches': lunches})

def dinner(request):
    dinners = Dinner.objects.all()
    return render(request, 'dinner.html', {'dinners': dinners})

def breakfast_detail(request, id):
    breakfast = get_object_or_404(Breakfast, pk=id)
    return render(request, 'breakfastdetail.html', {'breakfast': breakfast})

def lunch_detail(request, id):
    lunch = get_object_or_404(Lunch, pk=id)
    return render(request, 'lunchdetail.html', {'lunch': lunch})

def dinner_detail(request, id):
    dinner = get_object_or_404(Dinner, pk=id)
    return render(request, 'dinnerdetail.html', {'dinner': dinner})

# Views for adding menu items

def upload_breakfast(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        discount = request.POST.get('discount')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')  

       
        for owner in Owner.objects.all():
            if owner.username == request.user.username:
                break

        
        if not name or not price or not description or not discount or not rating or not image:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('upload_breakfast')

        
        try:
            discount = int(discount)
            rating = float(rating)
        except ValueError:
            messages.error(request, 'Invalid discount or rating value.')
            return redirect('upload_breakfast')

       
        new_breakfast = Breakfast(
            owner=owner,
            name=name,
            price=price,
            description=description,
            discount=discount,
            rating=rating,
            image=image  
        )
        new_breakfast.save()

        
        messages.success(request, 'Breakfast item uploaded successfully.')
        return redirect('dashboard') 

    return render(request, 'breakfastform.html')


def upload_lunch(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        discount = request.POST.get('discount')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')  
        spiciness_level = request.POST.get('spiciness_level')

        
        owner = None
        for owner in Owner.objects.all():
            if owner.username == request.user.username:
                break

        
        if not owner:
            messages.error(request, 'Owner not found.')
            return redirect('upload_lunch')

        
        if not name or not price or not description or not discount or not rating or not image or not spiciness_level:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('upload_lunch')

        
        try:
            discount = int(discount)
            rating = float(rating)
        except ValueError:
            messages.error(request, 'Invalid discount or rating value.')
            return redirect('upload_lunch')

        
        new_lunch = Lunch(
            owner=owner,
            name=name,
            price=price,
            description=description,
            discount=discount,
            rating=rating,
            image=image,  
            spiciness_level=spiciness_level  
        )
        new_lunch.save()

       
        messages.success(request, 'Lunch item uploaded successfully.')
        return redirect('dashboard')  

    return render(request, 'lunchform.html')

def upload_dinner(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        discount = request.POST.get('discount')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')  
        spiciness_level = request.POST.get('spiciness_level')
        chefs_special = request.POST.get('chefs_special') == 'on'  

       
        owner = None
        for owner in Owner.objects.all():
            if owner.username == request.user.username:
                break

        
        if not owner:
            messages.error(request, 'Owner not found.')
            return redirect('upload_dinner')

        
        if not name or not price or not description or not discount or not rating or not image or not spiciness_level:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('upload_dinner')

        
        try:
            discount = int(discount)
            rating = float(rating)
        except ValueError:
            messages.error(request, 'Invalid discount or rating value.')
            return redirect('upload_dinner')

        
        new_dinner = Dinner(
            owner=owner,
            name=name,
            price=price,
            description=description,
            discount=discount,
            rating=rating,
            image=image,  
            spiciness_level=spiciness_level,  
            chefs_special=chefs_special  
        )
        new_dinner.save()

        
        messages.success(request, 'Dinner item uploaded successfully.')
        return redirect('dashboard')  

    return render(request, 'dinnerform.html')

# Views for adding menu items to cart
@login_required (login_url='login')
def add_to_cart(request, item_type, item_id):
    product = None
    if item_type == 'breakfast':
        product = get_object_or_404(Breakfast, pk=item_id)
    elif item_type == 'lunch':
        product = get_object_or_404(Lunch, pk=item_id)
    elif item_type == 'dinner':
        product = get_object_or_404(Dinner, pk=item_id)
    else:
        return redirect('home')

    cart_item, created = Cart.objects.get_or_create(user=request.user, **{f'{item_type}': product}, defaults={'total_price': product.price, 'discount': 0})

    if not created:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * product.price
        cart_item.save()

    return redirect('view_cart')


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
    else:
        return redirect('view_cart')

    product_price = None
    if cart_item.breakfast:
        product_price = cart_item.breakfast.price
    elif cart_item.lunch:
        product_price = cart_item.lunch.price
    elif cart_item.dinner:
        product_price = cart_item.dinner.price

    if product_price is not None:
        cart_item.total_price = cart_item.quantity * product_price
        cart_item.save()

    return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

# Views for checkout
@login_required
def proceed_to_checkout(request):
 
    cart_items = Cart.objects.filter(user=request.user)
    
    
    for cart_item in cart_items:
       
        if cart_item.breakfast:
            owner = cart_item.breakfast.owner
        elif cart_item.lunch:
            owner = cart_item.lunch.owner
        elif cart_item.dinner:
            owner = cart_item.dinner.owner
        else:
            owner = None  
        
        
        Order.objects.create(
            user=request.user,
            owner=owner,
            breakfast=cart_item.breakfast,
            lunch=cart_item.lunch,
            dinner=cart_item.dinner,
            quantity=cart_item.quantity,
            total_price=cart_item.total_price,
            is_completed=False,
            is_cancelled=False
        )
        
        
        cart_item.delete()

    
    return redirect('checkout')

@login_required
def checkout(request):
    
    orders = Order.objects.filter(user=request.user, is_completed=False, is_cancelled=False)
    
    
    total_price = sum(order.total_price for order in orders)

    
    return render(request, 'checkout.html', {'orders': orders, 'total_price': total_price})

        
@login_required
def Purchase(request):
    
    user = request.user
    order_items = Order.objects.filter(user=user, is_completed=False)  
    total_price = sum(order.total_price for order in order_items)

    
    subject = 'Order Confirmation'
    email_template_name = 'confirmationemail.html'
    context = {
        'user': user,
        'order_items': order_items,
        'total_amount': total_price,
    }
    email_content = render_to_string(email_template_name, context)

   
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=email_content
    )

    
    order_items.update(is_completed=True)

    
    return redirect('orderconfirm')

def orderconfirm(request):
    return render(request, 'orderconfirm.html')