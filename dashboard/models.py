from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = 'Banner'
