from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    sucess_url = reverse_lazy('login')
    template_name = 'registration/signup.html'




