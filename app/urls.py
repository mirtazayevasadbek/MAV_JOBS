from django.urls import path

# from app.views import index, product_details, order_list, customers, order_details, add_product, customer_details, \
#     customer_add, customer_delete, customer_update, category, reset_password
# from app.views.auth import LogoutPage, RegisterPage, ForgotPasswordPage, ActivateEmailView, LoginPage
from app.views import index, login_page, RegisterPage, logout_page, blog_page, blog_detail_page, about_us_page , profile_page

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_page, name='login_page'),
    path('register/', RegisterPage.as_view(), name='register_page'),
    path('logout/', logout_page, name='logout_page'),
    path('blog/', blog_page, name='blog_page'),
    path('blog-detail/<int:job_id>', blog_detail_page, name='blog_detail_page'),
    path('about-us/', about_us_page, name='about_us_page'),
    path('profile/', profile_page, name='profile_page'),

]
