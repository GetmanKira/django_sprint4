""" содержит реализацию представлений для блога. 
включает в себя классы для создания, редактирования и удаления постов и комментариев,
а также для отображения различных страниц блога. Основное назначение данного файла — организовать
взаимодействие между пользователем и системой с использованием классов представлений,
обеспечивая функциональность и удобство использования.."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

NUMBER_OF_POSTS = 10#определение количества постов на странице


class AuthorView(UserPassesTestMixin):
    """Предоставляет доступ только автору объекта."""
    def test_func(self):
        return self.get_object().author == self.request.user# проверяет, что текущий пользователь - автор


class PostView(AuthorView, LoginRequiredMixin):
    """Представление для создания и редактирования постов."""
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id' #Ключевое слово для извлечения идентификатора поста из URL

    def handle_no_permission(self):
        """перенаправляет при отсутствии разрешения."""
        return redirect('blog:post_detail',
                        self.kwargs[self.pk_url_kwarg])# направляет на страницу поста

    def get_success_url(self):
        """URL для перенаправления после успешного выполнения формы."""
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
         """Добавление формы в контекст."""
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())# Передача формы с экземпляром поста
        return context


class CommentView(LoginRequiredMixin):
    """для создание и редактирование комментариев."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'#индентификатор комментария

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class IndexListView(ListView):
     """Представление для отображения списка постов на главной странице."""
    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS
    queryset = Post.objects.filter_posts_for_publication().count_comments()#запрос на получение потсов


class PostDetailView(ListView):
     """Представление для отображения деталей поста."""
    template_name = 'blog/detail.html'
    paginate_by = NUMBER_OF_POSTS

    def get_object(self):
         """Получение поста по идентификатору."""
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user == post.author:
            return post# если пользователь - автор, возвращает пост
        return get_object_or_404(Post.objects.filter_posts_for_publication(),
                                 pk=self.kwargs['post_id'])

    def get_queryset(self):
         """Получение комментариев к посту."""
        return self.get_object().comments.all()

    def get_context_data(self, **kwargs):
        """Добавление формы комментария и поста в контекст."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()#форма добавления комментария
        context['post'] = self.get_object()#текущиц пост 
        return context


class PostUpdateView(PostView, UpdateView):
    """Представление для обновления поста."""
    pass  # Унаследовано от PostView
    


class PostDeleteView(PostView, DeleteView):
    """Представление для удаления поста."""
    pass  # Унаследовано от PostView

class CommentCreateView(CommentView, CreateView):
     """Представление для создания нового комментария."""
    def form_valid(self, form):
         """Установка автора и поста перед сохранением."""
        form.instance.author = self.request.user # Установка текущего пользователя как автора комментария
        form.instance.post = get_object_or_404(
            Post.objects.filter_posts_for_publication(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CreatePostView(LoginRequiredMixin, CreateView):
    """Представление для создания нового поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class CommentUpdateView(CommentView, AuthorView, UpdateView):
    """Представление для обновления комментария."""
    pass  # Унаследовано от CommentView и AuthorView


class CommentDeleteView(CommentView, AuthorView, DeleteView):
    """Представление для удаления комментария."""
    pass  # Унаследовано от CommentView и AuthorVie


class CategoryDetailView(ListView):
    """Представление для отображения постов в определенной категории."""
    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS
    slug_url_kwarg = 'category_slug'# Ключевое слово для извлечения слага категории из URL

    def get_category(self):
        """Получение категории по слагу."""
        return get_object_or_404(
            Category, slug=self.kwargs[self.slug_url_kwarg], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()# Текущая категория
        return context

    def get_queryset(self):
         """Получение постов в категории."""
        return self.get_category().posts.filter_posts_for_publication()


class ProfileView(ListView):
    """Представление для отображения профиля пользователя."""
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS
    slug_url_kwarg = 'username'

    def get_profile(self):
        """Получение профиля пользователя по имени."""
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
          """Получение постов автора профиля."""
        author = self.get_profile()
        posts = author.posts.count_comments()  # Посты автора с подсчетом комментариев
        if author == self.request.user:
            return posts  # Если это текущий пользователь, возвращаем все посты
        return posts.filter_posts_for_publication()  # Иначе только опубликованные посты

    def get_context_data(self, **kwargs):
        """Добавление профиля в контекст."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""
    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'email')
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self, queryset=None):
         """Получение текущего пользователя."""
        return self.request.user

    def get_success_url(self):
         """URL для перенаправления после успешного редактирования профиля."""
        return reverse('blog:profile',
                       kwargs={'username': self.kwargs[self.slug_url_kwarg]})
