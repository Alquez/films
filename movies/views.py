from django.http import HttpResponse
from django.utils.html import format_html
from django.views import View
from django.db.models import Q
from .models import Movie, Rating, Genre, Comment
from django.views.generic import DetailView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage
from django.utils import timezone
from django.urls import reverse
from .forms import RatingForm, CommentForm


def success(request):
    return render(request, 'success.html')


def need_authenticate(request):
    return render(request, 'u_need_authenticate.html')


class HomeList(ListView):
    model = Movie
    template_name = 'movies.html'
    context_object_name = 'movies'
    ordering = ['-id']
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search_query')
        genre_slug = self.request.GET.get('genre')
        year = self.request.GET.get('year')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)

        if year:
            queryset = queryset.filter(year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_authenticated = self.request.user.is_authenticated
        is_premium = self.request.user.is_authenticated and self.request.user.is_premium

        genres = Genre.objects.all()
        genre_slug = self.request.GET.get('genre')
        year = self.request.GET.get('year')

        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            page = paginator.get_page(page_number)
        except InvalidPage:
            page = paginator.get_page(1)

        # Получить уникальные годы фильмов для фильтра по годам
        movie_years = Movie.objects.order_by('year').values_list('year', flat=True).distinct()

        context['movies'] = page
        context['is_authenticated'] = is_authenticated
        context['is_premium'] = is_premium
        context['genres'] = genres
        context['genre'] = genre_slug
        context['year'] = year
        context['movie_years'] = movie_years

        context['show_pagination'] = True

        return context


class MovieList(ListView):
    model = Movie
    template_name = 'movies.html'
    context_object_name = 'movies'


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next')
        slug = next_url.split('/')[-2]  # Получаем слаг из URL
        movie = get_object_or_404(Movie, slug=slug)  # Получаем фильм по слагу
        if request.user.is_authenticated:
            request.user.active_movie.add(movie)
        return render(request, 'success.html', {'movie': movie})


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_authenticated = request.user.is_authenticated
        is_premium = request.user.is_authenticated and request.user.is_premium
        form = RatingForm()

        if is_authenticated and request.user.premium_expiration and timezone.now() >= request.user.premium_expiration:
            request.user.is_premium = False
            request.user.save()

        if self.object.is_exclusive:
            if not is_authenticated:
                return HttpResponse(
                    "Это Премиум фильм, для того чтобы его посмотреть, зарегистрируйтесь и купите премиум-подписку "
                    "либо купите фильм")
            if self.object in request.user.active_movie.all():
                # Проверяем наличие оценки пользователя для данного фильма
                try:
                    rating = Rating.objects.get(user=request.user, movie=self.object)
                except Rating.DoesNotExist:
                    form = RatingForm()
            elif not is_premium:
                next_url = reverse('success') + '?next=' + request.get_full_path()
                link = format_html('<a href="{}">Купить фильм</a>.', next_url)
                message = format_html(
                    'Купите премиум-подписку и вам будет доступен просмотр фильма либо купите фильм {}', link)
                return HttpResponse(message)

        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # перенаправление на страницу входа

        self.object = self.get_object()
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                user=request.user,
                movie=self.object,
                defaults={'star': form.cleaned_data['star']}
            )
            if not created:
                rating.star = form.cleaned_data['star']
                rating.save()
            if rating is None:
                rating = None

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            message = comment_form.cleaned_data['message']
            comment = Comment(movie=self.object, name=name, message=message)
            comment.save()

        return redirect('movie_detail', slug=self.object.slug)
