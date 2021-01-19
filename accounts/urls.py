from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login
    path('login', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register', views.logoutUser, name='register'),

    #  main
    path('', views.home, name='home'),

    # password
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password/password_reset_done.html"), name="password_reset_complete"),

    # User Pages
    path('create_user', views.create_customer, name='create_customer'),
    path('user_profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('user_details/<str:pk>/', views.user_details, name='user_details'),
    path('user_update_phone/<str:pk>/', views.user_update_phone, name='user_update_phone'),
    path('customer_add_bank/<str:pk>/', views.customer_add_bank, name='customer_add_bank'),
    path('customer_add_bank1/<str:pk>/', views.customer_add_bank1, name='customer_add_bank1'),
    path('customer_add_game/<str:pk>/', views.customer_add_game, name='customer_add_game'),
    

    # link User
    path('list_user', views.list_user, name='list_user'),
    path('follow_ups', views.follow_ups, name='follow_ups'),
    path('blacklist_bank', views.blacklist_bank, name='blacklist_bank'),

    # Link Transaction
    path('list_deposit', views.list_deposit, name='list_deposit'),
    path('list_withdrawal', views.list_withdrawal, name='list_withdrawal'),
    path('list_transfer', views.list_transfer, name='list_transfer'),
    path('list_4d', views.list_4d, name='list_4d'),
    path('list_weekly', views.list_weekly, name='list_weekly'),
    
    # Link Report
    path('report_sale', views.report_sale, name='report_sale'),
    path('report_transaction', views.report_transaction, name='report_transaction'),

    # Link Setting
    path('manage_game', views.manage_game, name='manage_game'),
    path('manage_bank', views.manage_bank, name='manage_bank'),
    path('manage_referral', views.manage_referral, name='manage_referral'),
    path('manage_promotion', views.manage_promotion, name='manage_promotion'),
    path('manage_max_withdrawal', views.manage_max_withdrawal, name='manage_max_withdrawal'),
    path('manage_success_messages/<str:pk>', views.manage_success_messages, name='manage_success_messages'),

    # Link Employee
    path('manage_employee', views.manage_employee, name='manage_employee'),
    path('manage_position', views.manage_position, name='manage_position'),
    path('action_logs', views.action_logs, name='action_logs'),

    #Navbar 
    path('search_user', views.search_user, name='search_user'),
    path('kiosk', views.kiosk, name='kiosks'),

    #SMS
    path('sms_not_include', views.sms_not_include, name='sms_not_include'),
    path('sms', views.sms, name='sms'),
    
    #functions
    path('refresh_dashboard', views.refresh_dashboard, name='refresh_dashboard'),
    path('transactionStatus/<str:pk>/<str:status>', views.transactionStatus, name='transaction_status'),
    path('newWithdrawalLimit/', views.newWithdrawalLimit, name='newWithdrawalLimit'),
    path('depositconfirm/<str:pk>/', views.depositconfirm, name='deposit_confirm'),
    path('depositconfirmAfter/<str:pk>/<str:completed>', views.depositconfirmAfter, name='deposit_confirm_after'),
    path('language_change/<str:pk>/<str:language>', views.language_change, name='language_change'),

    #? Transaction Control    
    path('createTransaction/<str:pk>/<str:pk_type>', views.createTransaction, name='create_transaction'),
    path('editTransaction/<str:pk>/<str:pk_type>', views.editTransaction, name='edit_transaction'),
    
    #? Add_new
    path('createBank', views.createBank, name='add_bank'),
    path('createGame', views.createGame, name='add_game'),
    path('createReferral', views.createReferral, name='add_referral'),
    path('createPromotion', views.createPromotion, name='add_promotion'),

    #? Edit
    # path('editBank', views.editBank, name='edit_bank'),
    path('editReferral/<str:pk>/', views.editReferral, name='edit_referral'),
    path('editBank/<str:pk>/', views.editBank, name='edit_bank'),
    path('editGame/<str:pk>/', views.editGame, name='edit_game'),
    path('editPromotion/<str:pk>/', views.editPromotion, name='edit_promotion'),

    #? Credit
    path('creditGameAdd/<str:pk>/', views.creditGameAdd, name='credit_game_add'),
    path('creditGameWeekly/<str:pk>/<str:amount>/', views.creditGameWeekly, name='credit_game_weekly'),
    path('creditGameticket/<str:pk>/', views.creditGameticket, name='credit_game_ticket'),
    path('creditGameDeduct/<str:pk>/', views.creditGameDeduct, name='credit_game_deduct'),

    #? Transactions profile
    path('deposit_profile/<str:pk>/', views.deposit_profile, name='deposit_profile'),
    path('withdrawal_profile/<str:pk>/', views.withdrawal_profile, name='withdrawal_profile'),
    path('transfer_profile/<str:pk>/', views.transfer_profile, name='transfer_profile'),

    #? dashboard function
    path('withdrawal_bank/<str:pk>/', views.withdrawal_bank, name='withdrawal_bank'),

    #? delete
    path('delete_promotion/<str:pk>/', views.delete_promotion, name='delete_promotion'),
    path('delete_game/<str:pk>/', views.delete_game, name='delete_game'),
    path('delete_customergame/<str:pk>/', views.delete_customergame, name='delete_customergame'),
    path('delete_customerbank/<str:pk>/', views.delete_customerbank, name='delete_customerbank'),



    # un-use
    # path('user/', views.userPage, name='user'),
    # path('register/', views.registerPage, name='register'),
    # path('createOrder/<str:pk>', views.createOrder, name='create_order'),
    # path('updateOrder/<str:pk>/', views.updateOrder, name='update_order'),
    # path('deleteOrder/<str:pk>/', views.deleteOrder, name='delete_order'),
    # path('account/', views.accountSettings, name='account'),
    # path('products/', views.products, name='product'),
    # path('user/<str:pk>/', views.customer, name='customer'),
    
]





