from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from app.forms import LoginForm, RegisterForm
from app.models import User, Job


class CreateUser(FormView):
    form_class = User
    success_url = None
    template_name = None


def index(request):
    return render(request, 'app/index.html')


def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
            return redirect('index')
        else:
            messages.add_message(
                request,
                level=messages.ERROR,
                message='Loginda xatolik'
            )
    return render(request, 'app/login.html', {'form': form})


class RegisterPage(FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('login_page')
    template_name = 'app/register.html'

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            level=messages.WARNING,
            message='Successfully registreted:) '
        )
        return super().form_valid(form)


def logout_page(request):
    return render(request, 'app/logout.html')


def blog_page(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'app/blog.html', context)


def blog_detail_page(request, job_id):
    jobs = Job.objects.filter(id=job_id).first()
    context = {
        'jobs_details': jobs
    }
    return render(request, 'app/single-post.html', context)


def about_us_page(request):
    return render(request, 'app/aboutus.html')


def profile_page(request):
    return render(request, 'app/profile.html')
