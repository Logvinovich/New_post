from django.db import models
from News_Portal.resources import VARIANT
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authoruser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingauthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postr = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_r = 0
        p_r += postr.get('postRating')

        commentr = self.authoruser.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_r = 0
        c_r += commentr.get('commentRating')

        self.ratingauthor = p_r * 3 + c_r
        self.save()

    def __str__(self):
        return f"{self.authoruser}"

class Category(models.Model):
    name_category = models.CharField(max_length = 64, unique = True)

    def __str__(self):
        return f"{self.name_category}"

class Post(models.Model):
    news = 'NS'
    topic = 'TP'
    choise = models.CharField(max_length=2, choices=VARIANT, default=topic)
    createpost_datetime = models.DateTimeField(auto_now_add = True)
    head_text = models.CharField(max_length=255, default= "Заголовок")
    body_text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category,through='PostCategory')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.body_text[0:123] + '...'

    def __str__(self):
        dataf = 'Post from {}'.format(self.createpost_datetime.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.head_text}"

class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.post},from the category:  {self.category}"

class Comment(models.Model):
    comment_text = models.TextField()
    createcom_datetime = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)
    userpost = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.createcom_datetime}, {self.userpost}"