from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="home"),
    path(
        "categoria/<slug:slug>/",
        views.CategoryArticleListView.as_view(),
        name="category_detail",
    ),
    path(
        "articulo/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
]
