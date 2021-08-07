from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    sucess_url = reverse_lazy('accounts/login')
    template_name = 'registration/signup.html'




