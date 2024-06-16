from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    NOTE = {
        'title': 'Новая заметка',
        'text': 'Текст новой заметки'
    }

    SLUG = {
        'slug': 'test_slug'
    }

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Author')
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.login_url = reverse('users:login')

    def test_user_can_create_note_with_slug(self):

        self.client.force_login(self.author)

        response = self.client.post(self.add_url, {**self.NOTE, **self.SLUG})

        self.assertRedirects(response, self.success_url)
        self.assertTrue(Note.objects.filter(slug=self.SLUG['slug']).exists())

    def test_user_can_create_note_without_slug(self):

        self.client.force_login(self.author)

        response = self.client.post(self.add_url, self.NOTE)

        self.assertRedirects(response, self.success_url)
        self.assertTrue(Note.objects.filter(title=self.NOTE['title']).exists())

    def test_note_slug_is_unique(self):

        self.client.force_login(self.author)

        response1 = self.client.post(self.add_url, {**self.NOTE, **self.SLUG})
        notes_count = Note.objects.filter(slug=self.SLUG['slug']).count()

        response2 = self.client.post(self.add_url, {**self.NOTE, **self.SLUG})

        self.assertFormError(
            response2,
            form='form',
            field='slug',
            errors=f'{self.SLUG["slug"]}{WARNING}'
        )
        self.assertRedirects(response1, self.success_url)
        self.assertEqual(Note.objects.filter(
            slug=self.SLUG['slug']).count(), notes_count)

    def test_anonymous_user_cannot_create_note(self):

        response = self.client.post(self.add_url, self.NOTE)

        self.assertRedirects(response, f'{self.login_url}?next={self.add_url}')
        self.assertFalse(Note.objects.filter(
            title=self.NOTE['title']).exists())


class TestNoteEditDelete(TestCase):

    TITLE = 'Новая заметка'
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённый текст'

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.other_author = User.objects.create(username='Reader')
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)

        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.NOTE_TEXT,
            slug='new_note',
            author=cls.author
        )

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')

        cls.form_data = {
            'title': cls.TITLE,
            'text': cls.NEW_NOTE_TEXT}

    def test_author_can_delete_note(self):

        initial_notes_count = Note.objects.count()

        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)

        final_notes_count = Note.objects.count()
        self.assertEqual(final_notes_count, initial_notes_count - 1)

    def test_other_author_cant_delete_note(self):

        initial_notes_count = Note.objects.count()

        response = self.other_author_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        final_notes_count = Note.objects.count()
        self.assertEqual(final_notes_count, initial_notes_count)

    def test_author_can_edit_note(self):

        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)

        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):

        response = self.other_author_client.post(
            self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
