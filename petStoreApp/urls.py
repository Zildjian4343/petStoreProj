

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("petDetails/<int:pid>", views.petDetails, name="petDetails"),

    path('edit/user/', views.edit_user, name='edit_user'),
     path('profile/', views.profile, name='profile'),

    path("viewCart/", views.viewCart, name="viewCart"),
    path("addCart/<int:pid>", views.addCart, name="addCart"),
    path("removeCart/<int:pid>", views.removeCart, name="removeCart"),
    path("search/", views.search, name="search"),
    path("range", views.range, name="range"),
    path("catlist", views.catlist, name="catlist"),
    path("doglist", views.doglist, name="doglist"),
    path("Collars", views.Collars, name="Collars"),
    path("Toys", views.Toys, name="Toys"),
    path("Foods", views.Foods, name="Foods"),
    path("Grooming", views.Grooming, name="Grooming"),
    path("Clothing", views.Clothing, name="Clothing"),
    path("Health", views.Health, name="Health"),
    path("Housing", views.Housing, name="Housing"),

######################
    path('payment-success/<int:product_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:product_id>/', views.PaymentFailed, name='payment-failed'),
    path('cart/', views.cart_view, name='cart'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('receipt/', views.receipt, name='receipt'),

    path('grooming_reservation/', views.grooming_reservation, name='grooming_reservation'),
    path('reservation_success/', views.reservation_success, name='reservation_success'),


    path("priceOrder", views.priceOrder, name="priceOrder"),
    path("descpriceOrder", views.descpriceOrder, name="descpriceOrder"),
    path("updateqty/<int:uval>/<int:pid>", views.updateqty, name="updateqty"),
    path("viewOrder", views.viewOrder, name="viewOrder"),
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("myOrder/", views.myOrder, name="myOrder"),
    path("insertProduct/", views.insertProduct, name="insertProduct"),
    
    path('appointment-status/',views.view_appointments, name='appointment_status'),

    
    
    # Admin
   
    path("adminn/", views.admin_dashboard, name="admin_dashboard"),
    path('update_payment_status/', views.update_payment_status, name='update_payment_status'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),
    path('mark_completed/<int:order_id>/', views.mark_completed, name='mark_completed'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('settings/', views.setting, name='settings'), 
    
    
    #Payment 
     path('process_payment/', views.process_payment, name='process_payment'),
    path('make_payment/', views.make_payment, name='make_payment'),  # Assuming make_payment view exists
    path('payment_success/', views.payment_success, name='payment_success'),  # Assuming a success view exists
    
    


]
