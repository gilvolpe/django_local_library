from unittest.util import _MAX_LENGTH

from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction')

    def __str__(self) -> str:
        return self.name

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
    
    
from django.urls import reverse


class Book(models.Model):
    title   = models.CharField(max_length=200)
    author  = models.ForeignKey('Author',on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000,help_text='Enter a brief description of the book') 
    isbn    = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre   = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])  # type: ignore
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    
import uuid
from datetime import date

from django.contrib.auth.models import User


class BookInstance(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book     = models.ForeignKey('Book',on_delete=models.RESTRICT, null = True)
    imprint  = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m','Maintance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='m',
        help_text='Book Availability' )
    
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ['due_back']

    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'  # type: ignore
    
    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    
class Author(models.Model):
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])  # type: ignore

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'