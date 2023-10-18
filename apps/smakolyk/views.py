from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, redirect

from apps.smakolyk.forms import ProfileUpdateForm


class ProfileView(CreateView):
    template_name = 'apps.smakolyk/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EditProfileView(UpdateView):
    form_class = ProfileUpdateForm
    template_name = "apps.smakolyk/update_profile.html"
    slug_url_kwarg = 'slug'
    success_url = 'profile'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.userprofile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,
                               request.FILES,
                               instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})
