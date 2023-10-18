from django.views.generic import CreateView
from django.shortcuts import render


class ProfileView(CreateView):
    template_name = 'apps.smakolyk/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
