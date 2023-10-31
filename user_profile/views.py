from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy


@login_required
def profile(request):
    return render(request, 'user_profile/user_profile.html')


class ShowProfilePageView(DetailView):
    model = profile
    template_name = 'user_profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = profile
    template_name = 'user_profile/create_profile.html'
    fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


success_url = reverse_lazy('tasks')
