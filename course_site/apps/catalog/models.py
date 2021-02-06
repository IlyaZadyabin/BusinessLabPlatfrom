from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique course instances
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

from course_site import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Page(models.Model):
    number = models.IntegerField(null=True, blank=True)
    course = models.ForeignKey('Course', related_name="pages", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(help_text="Enter a course content", blank=True)


class Course(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    summary2 = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    summary3 = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    added_by = models.ForeignKey(User,
                                 null=True, blank=True, on_delete=models.SET_NULL, related_name="course_added_by")
    attendants = models.ManyToManyField(User, null=True, blank=True)
    #  pages = models.ManyToManyField(Page, null=True, blank=True, related_name="page")
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text='Book availability')

    def amount_of_pages(self, *args, **kwargs):
        return self.pages.count()

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.title)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('course-detail', args=[str(self.id)])


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)
