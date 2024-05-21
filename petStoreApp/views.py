from django.shortcuts import render, redirect,get_object_or_404
from .models import Pet, CartItem, Order, User,GroomingReservation
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm, AddPet
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import EditUserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib.auth import update_session_auth_hash



import random
from django.contrib.auth.decorators import user_passes_test

def setting(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Update the session authentication hash
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'settings.html', {'form': form})
    else:
        return redirect('login') 

def user_is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(user_is_admin)
def admin_dashboard(request):
    pets_count = Pet.objects.count()
    cart_items_count = CartItem.objects.count()
    orders_count = Order.objects.count()
    total_sales = Order.objects.aggregate(total_sales=Sum('pet__price'))['total_sales'] or 0
    total_users = User.objects.count()

    sales_data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'data': [5000, 10000, 15000, 20000, 25000, 30000]  
    }
    users_data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'data': [100, 200, 300, 400, 500, 600]  
    }

    pets = Pet.objects.all()
    cart_items = CartItem.objects.select_related('pet').all()
    orders = Order.objects.select_related('user', 'pet').all()  
    customers = User.objects.all()

    # Fetch grooming appointments
    grooming_appointments = GroomingReservation.objects.all()

    context = {
        'pets_count': pets_count,
        'cart_items_count': cart_items_count,
        'orders_count': orders_count,
        'total_sales': total_sales,
        'total_users': total_users,
        'sales_data': sales_data,
        'users_data': users_data,
        'pets': pets,
        'cart_items': cart_items,
        'orders': orders,
        'customers': customers,  # Add customers to context
        'appointments': grooming_appointments,  # Add grooming appointments to context
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to user's profile page after editing
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'edit_user.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def update_payment_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_status = request.POST.get('payment_status')
        
        if order_id and payment_status:
            order = Order.objects.filter(order_id=order_id).first()
            if order:
                order.payment_status = payment_status
                order.save()
                messages.success(request, 'Payment status updated successfully!')
                return redirect('admin_dashboard_content')  # Redirect to the admin dashboard
            else:
                messages.error(request, 'Invalid order ID!')
        else:
            messages.error(request, 'Invalid data submitted!')

    return redirect('admin_dashboard') 



# Create your views here.
def index(request):
    pet = Pet.objects.all()
    context = {'pet': pet}
    return render(request, 'index.html', context)



def petDetails(req, pid):
    pet = Pet.objects.get(pet_id=pid)
    context = {}
    context["pet"] = pet
    return render(req, "petDetail.html", context)


    
def viewCart(req):
    if req.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=req.user)
    else:
        cart_item = CartItem.objects.filter(user=None)
        messages.warning(req, "Log in to add to cart")
    context = {}
    context["items"] = cart_item
    total_price = 0
    for x in cart_item:
        total_price += x.pet.price * x.quantity
    context["total"] = total_price
    length = len(cart_item)
    context["length"] = length
    return render(req, "cart.html", context)


def addCart(req, pid):
    pet = Pet.objects.get(pet_id=pid)
    user = req.user if req.user.is_authenticated else None
    if user:
        cart_item, created = CartItem.objects.get_or_create(pet=pet, user=user)
    else:
        return redirect("/login")
    print(cart_item, created)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect("/viewCart")


def removeCart(req, pid):
    pet = Pet.objects.get(pet_id=pid)
    cart_item = CartItem.objects.filter(pet=pet, user=req.user)
    cart_item.delete()
    return redirect("/viewCart")

from django.contrib.auth.decorators import login_required

@login_required
def receipt(request):
    # Fetch orders related to the user
    orders = Order.objects.filter(user=request.user)

    # Calculate total items and total price
    total_items = 0
    total_price = 0
    for order in orders:
        total_items += order.quantity
        total_price += order.quantity * order.pet.price

    context = {
        'user': request.user,
        'items': orders,
        'total_items': total_items,
        'total_price': total_price,
    }
    return render(request, 'receipt.html', context)



def cancel_order(request, order_id):
    orders = Order.objects.filter(order_id=order_id)
    for order in orders:
        order.delete()
    return redirect('admin_dashboard')

from django.db.models import Q


def search(req):
    query = req.POST["q"]
    print(f"Query is {query}")
    if not query:
        result = Pet.objects.all()
    else:
        result = Pet.objects.filter(
            Q(product_name__icontains=query)
            | Q(category__icontains=query)
            | Q(price__icontains=query)
        )
    return render(req, "search.html", {"results": result, "query": query})


def range(req):
    if req.method == "GET":
        return redirect("/")
    else:
        min = req.POST["min"]
        max = req.POST["max"]
        if min != "" and max != "" and min is not None and max is not None:
            queryset = Pet.pet.get_price_range(min, max)
            context = {}
            context["pet"] = queryset
            return render(req, "index.html", context)
        else:
            return redirect("/")


def catlist(req):
    if req.method == "GET":
        queryset = Pet.pet.catlist()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)


def doglist(req):
    if req.method == "GET":
        queryset = Pet.pet.doglist()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)


def Collars(req):
    if req.method == "GET":
        queryset = Pet.pet.Collars()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)


def Toys(req):
    if req.method == "GET":
        queryset = Pet.pet.Toys()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
    
def Foods(req):
    if req.method == "GET":
        queryset = Pet.pet.Foods()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
    
def Grooming(req):
    if req.method == "GET":
        queryset = Pet.pet.Grooming()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
def Clothing(req):
    if req.method == "GET":
        queryset = Pet.pet.Clothing()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
    
def Health(req):
    if req.method == "GET":
        queryset = Pet.pet.Health()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
    
def Housing(req):
    if req.method == "GET":
        queryset = Pet.pet.Housing()
        context = {}
        context["pet"] = queryset
        return render(req, "index.html", context)
    
################################################################################
def priceOrder(req):
    queryset = Pet.objects.all().order_by("price")
    context = {}
    context["pet"] = queryset
    return render(req, "index.html", context)


def descpriceOrder(req):
    queryset = Pet.objects.all().order_by("-price")
    context = {}
    context["pet"] = queryset
    return render(req, "index.html", context)


def updateqty(req, uval, pid):
    pets = Pet.objects.get(pet_id=pid)
    a = CartItem.objects.filter(pet=pets)
    print(a)
    print(a[0])
    print(a[0].quantity)
    if uval == 1:
        temp = a[0].quantity + 1
        a.update(quantity=temp)
    else:
        temp = a[0].quantity - 1
        a.update(quantity=temp)
    return redirect("viewCart")


def viewOrder(req):
    cart_item = CartItem.objects.filter(user=req.user)
    print(cart_item)
    oid = random.randrange(1000, 9999)
    for x in cart_item:
        Order.objects.create(
            order_id=oid,
            pet_id=x.pet.pet_id,
            quantity=x.quantity,
            user=req.user,
        )
        # x.delete()
    orders = Order.objects.filter(user=req.user, is_completed=False)
    context = {}
    context["items"] = orders
    total_price = 0
    for x in orders:
        print(x.pet.price, x.quantity)
        total_price += x.pet.price * x.quantity
        print(total_price)
    context["total"] = total_price
    length = len(orders)
    context["length"] = length
    return render(req, "viewOrder.html", context)


def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, ("User created successfully"))
            return redirect("/")
        else:
            messages.error(req, ("Incorrect Username or Password Format"))
    context = {"form": form}
    return render(req, "register.html", context)


def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, ("Logged in Successfully"))
            return redirect("/")
        else:
            messages.error(req, ("There is error"))
            return redirect("/login")
    else:
        return render(req, "login.html")


def logout_user(req):
    logout(req)
    messages.success(req, ("Logged out Successfully"))
    return redirect("/")



def myOrder(req):
    orders = Order.objects.filter(user=req.user, is_completed=True)
    context = {}
    context["items"] = orders
    return render(req, "my_order.html", context)


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def insertProduct(req):
    if req.user.is_authenticated:
        user = req.user
        if req.method == "GET":
            form = AddPet()
            return render(req, "insertPet.html", {"form": form, "username": user})
        else:
            form = AddPet(req.POST, req.FILES or None)
            if form.is_valid():
                form.save()
                return redirect("/")
            else:
                return render(req, "insertPet.html", {"form": form, "username": user})
    else:
        return redirect("/login")


    
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def payment_invoice(request):
    if request.method == 'POST':
        total_price = request.POST.get('total_price')
        if not total_price:
            return HttpResponse("Total price is required.", status=400)

        # Dummy invoice content for demonstration
        invoice_content = f"Invoice for {request.user.username}\nTotal Price: ${total_price}"

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="invoice.txt"'
        response.write(invoice_content)
        return response

    else:
        items = []  # Replace this with your logic to fetch cart items
        total = 0  # Replace this with your logic to calculate total price
        context = {
            'user': request.user,
            'items': items,
            'length': len(items),
            'total': total,
        }
        return render(request, 'invoice.html', context)
    
    
    
def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('index')  # Redirect to the cart page if cart is empty

        # Create orders based on cart items
        for item in cart_items:
            order = Order.objects.create(
                order_id=item.pet.pet_id,  # Use pet_id as the order_id for simplicity
                pet=item.pet,
                quantity=item.quantity,
                user=user
            )
            order.save()

        # Clear the cart after placing the order
        CartItem.objects.filter(user=user).delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('my_orders')  # Redirect to the "My Orders" page
    else:
        messages.error(request, 'Error: Invalid request!')
        return redirect('index') 
    
    
def my_orders(request):
    orders = Order.objects.filter(user=request.user)  # Fetch orders for the current user
    context = {'orders': orders}
    return render(request, 'my_orders.html', context)

#### CHECKOUT ######################################################################################




def PaymentSuccessful(request,pet_id ):
    
    
    pet = Pet.objects.get(id=pet_id)

    return render(request, 'payment_successful.html', {'pet': pet})
    
    
def PaymentFailed(request,pet_id ):
    
    pet = Pet.objects.get(id=pet_id)

    return render(request, 'payment_failed.html', {'pet': pet})



    
    
def cart_view(request):
    # Retrieve the user's cart items
    if request.user.is_authenticated:
        cart_items = Order.objects.filter(user=request.user, is_completed=False)
    else:
        cart_items = None  
    
    total_items = 0
    total_price = 0
    if cart_items:
        for item in cart_items:
            total_items += item.quantity
            total_price += item.quantity * item.pet.price
    
    # Pass cart items, total price, and total items to the template
    return render(request, 'cart.html', {'items': cart_items, 'total': total_price, 'length': total_items})

def view_orders(request):
    # Retrieve all orders for the current user
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = None  
    
    return render(request, 'index.html', {'orders': orders})



from .models import Pet
from .forms import AddPet

def add_pet(request):
    if request.method == 'POST':
        form = AddPet(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AddPet()
    return render(request, 'add_pet.html', {'form': form})

def add_pet_success(request):
    form = AddPet()
    return render(request, 'add_pet.html', {'form': form, 'success': True})


def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == 'POST':
        form = AddPet(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AddPet(instance=pet)
    return render(request, 'edit_pet.html', {'form': form})


def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_pet.html', {'pet': pet})


def mark_completed(request, order_id):
    orders = Order.objects.filter(order_id=order_id)
    for order in orders:
        order.is_completed = True
        order.save()
    return redirect('admin_dashboard')



#################### PAYMENT #######################################################################
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order
from django.core.files.storage import FileSystemStorage


def payment_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'payment_confirmation.html', {'order': order})


from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string

def payment_success(request):
    return render(request, 'payment_success.html')

def make_payment(request):
    return render(request, 'make_payment.html')


from .models import Profile
from django.core.exceptions import ObjectDoesNotExist

def process_payment(request):
    if request.method == 'POST':
        payment_amount = request.POST['paymentAmount']
        email = request.POST['email']
        reference_number = request.POST['referenceNumber']
        payment_screenshot = request.FILES['paymentScreenshot']
        
        # Save the uploaded screenshot
        fs = FileSystemStorage()
        screenshot_name = fs.save(payment_screenshot.name, payment_screenshot)
        screenshot_path = fs.path(screenshot_name)
        screenshot_url = fs.url(screenshot_name)
        
        try:
            # Retrieve the profile associated with the user
            profile = Profile.objects.get(user=request.user)
            mobile_number = profile.mobile_number
        except ObjectDoesNotExist:
            # Handle the case where profile doesn't exist
            mobile_number = None
        
        # Prepare context for the email
        context = {
            'payment_amount': payment_amount,
            'email': email,
            'reference_number': reference_number,
            'mobile_number': mobile_number,
            'screenshot_url': screenshot_url,
        }
        
        # Send receipt email to customer
        subject = 'Payment Receipt'
        customer_message = render_to_string('receipt_email.txt', context)
        customer_email = EmailMessage(
            subject,
            customer_message,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        customer_email.attach_file(screenshot_path)
        customer_email.send()

        # Optionally, send the same email to the admin
        admin_email = settings.ADMIN_EMAIL
        admin_message = render_to_string('admin_receipt_email.html', context)
        admin_email_message = EmailMessage(
            subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email]
        )
        admin_email_message.attach_file(screenshot_path)
        admin_email_message.send()
        
        return redirect('payment_success')  
    return redirect('make_payment')



from .forms import GroomingReservationForm 

def grooming_reservation(request):
    if request.method == 'POST':
        form = GroomingReservationForm(request.POST)
        if form.is_valid():
            # Save the form with the current user as the owner
            grooming_reservation = form.save(commit=False)
            grooming_reservation.user = request.user 
            grooming_reservation.save()
    else:
        form = GroomingReservationForm()

    user_grooming_orders = GroomingReservation.objects.filter(user=request.user)

    return render(request, 'grooming_reservation.html', {'form': form, 'user_grooming_orders': user_grooming_orders})


def reservation_success(request):
    return render(request, 'reservation_success.html')



@login_required
def view_appointments(request):
    if request.method == 'POST':
        form = GroomingReservationForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('appointment_status') 
    else:
        form = GroomingReservationForm()
    return render(request, 'appointment_status.html', {'form': form})


