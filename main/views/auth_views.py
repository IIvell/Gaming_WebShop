from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser:
            return redirect('/admin')
        return super().form_valid(form)