from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique course instances
from django.contrib.auth.models import User
from datetime import date

from course_site import settings


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Page(models.Model):
    number = models.IntegerField(null=True, blank=True)
    course = models.ForeignKey('Course', related_name="pages", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(max_length=1000, help_text="Enter a course content", blank=True)


class Course(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book", blank=True)

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


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the coursec's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
