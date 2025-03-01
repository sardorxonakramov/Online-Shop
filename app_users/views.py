from django.urls import reverse_lazy
from django.views.generic  import CreateView,UpdateView
from django.contrib.auth import get_user_model


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import UserRegisterForm,UserUpdateForm

User = get_user_model()


# Create your views here.
class registrationView(CreateView):
    model = User
    template_name = "app_users/registration.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')




@login_required
def accountView(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Foydalanuvchi ma'lumotlarini saqlash
            form.save()
            password1 = form.cleaned_data.get('password1')

            # Agar parol yangilangan bo'lsa, sessiyani yangilab turish
            if password1:
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been updated successfully!")
            else:
                messages.success(request, "Your account information has been updated successfully!")

            # Sahifani qayta yo'naltirish (reflesh qilish)
            return redirect(reverse('account'))
        else:
            messages.error(request, "There was an error updating your account. Please try again.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'app_users/account.html', {'form': form})

