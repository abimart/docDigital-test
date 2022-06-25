from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import re

class Client(models.Model):
    #nombre, RFC, teléfono

    def validate_rfc(value):
        reg = re.compile('^([a-zA-Z&Ñ]{3,4}\d{6}[a-zA-Z0-9]{3})$')
        if not reg.match(value) :
            raise ValidationError(u'%s RFC invalido' % value)

    name = models.CharField(max_length=50)
    rfc = models.CharField(max_length=13,
                            validators=[validate_rfc])
    telefono = models.CharField(max_length=10, null=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.name)

            has_slug = Client.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.name) + '-' + str(count) 
                has_slug = Client.objects.filter(slug=slug).exists()

            self.slug = slug
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

