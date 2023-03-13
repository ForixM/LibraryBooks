from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import HttpResponseRedirect
from book.models import Wallet

# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = "registration/signup.html"

    def form_valid(self, form):
        self.object = form.save()
        wallet = Wallet(owner=self.object, balance=50.0)
        wallet.save()
        return HttpResponseRedirect(self.get_success_url())
