# YaNote
### YaNews is an online notebook where users can leave their notes so that they don't forget anything.

## Project description

* The main page of the project is accessible to any user.
* The page with list of all notes is accessible only to authorized users. It displays all notes as a numbered list of note titles, in ascending chronological order (from oldest to latest).
* Each note has its own page, with the title and full text of the note. This page's http address contains unique slug chosen by the user when this note is created.
* Any user can register on the site independently.

### Project tech stack:

Python, Django, HTML, SQLlite3, pytest, unittest

## unittest tests for YaNote:

### In file test_routes.py:
* Main page, login/logout/sign-up pages are all accessible to an anonymous user.
* Unauthorized user cannot access the pages for note details, editing or deleting note (error 404 is returned).
* Note details, deletion and editing pages are available only to authorized user.
* When trying to load the note details, edit or delete page, the anonymous user is redirected to the authorization page.

### In file test_content.py:
* Notes of each user are shown to this user only. Notes of other users are inaccessible.
* Note is added / edited via dedicated form.
* Page with the list of all notes shows all existing notes (no pagination).
* Notes in the list are sorted in ascending chronological order: old ones at the beginning of the list, new ones - at the end.

### In file test_logic.py_:
* Users can create notes with or without slug.
* Note slug is unique.
* Unauthorized user cannot create note.
* Authorized user can edit or delete his/her/their notes.
* Authorized user cannot edit or delete other people's notes.

### How to run the project:

Clone repository and switch to project directory using command line:

```
git@github.com:kopf8/ya_note.git
```

```
cd ya_note
```

Create & activate virtual environment:

```
python -m venv env
```

* For Linux/macOS:

    ```
    source env/bin/activate
    ```

* For Win:

    ```
    source env/Scripts/activate
    ```

Upgrade pip:

```
python -m pip install --upgrade pip
```

Create .env file and fill it as per example:

```
SECRET_KEY = <your-secret-key>
```

Install project requirements from file _requirements.txt_:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Load fixtures:

```
python manage.py loaddata notes.json
```

Run project:

```
python manage.py runserver
```

Run project tests:
* Pytest:

    ```
    pytest
    ```

* Unittest:

    ```
    python manage.py test notes.tests
    ```

### Author:
**Maria Kirsanova**<br>
Github profile — https://github.com/kopf8