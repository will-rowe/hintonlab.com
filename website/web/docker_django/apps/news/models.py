from django.db import models
from django.utils import timezone

class Post(models.Model):
    CATEGORY = (
    ('Lab-News', 'Lab-News'),
    ('Social', 'Social'),
    ('Other', 'Other'),
    )

    ORIENTATION = (
    ('L', 'L'),
    ('P', 'P'),
    )

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(upload_to='news_blog_imgs', blank=False)
    picture_caption = models.CharField(max_length=400, blank=True)
    picture_orientation = models.CharField(max_length=1,choices=ORIENTATION,default='L')
    category = models.CharField(max_length=10,choices=CATEGORY,default='Lab-News')

    # define methods for Post object
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# register model for watson searching
from watson import search as watson
watson.register(Post)
