# forum

**forum** is a web application that allow users to interact with each other by sharing posts, engaging in conversations in the post reply session and gathering in groups. It is built on Django 4.2, stylized with Bootstrap 5.3 and implements PostgreSQL as its database.

You can access **forum** right now! Just click [here](https://djangoforum-production.up.railway.app/).

## Features

- Built with the Django 4.2, a powerful and popular Python framework for building web applications.
- Styled with Bootstrap, a widely-used CSS library that provides a range of customizable components and styles for building modern web interfaces.
- Integration of PostgreSQL, a robust and scalable database system, for efficient data management and retrieval.

With **forum** you can:

- Create posts and reply to other users' posts and comments.
- Create and manage groups: invite people to join, with the option to generate a one-time use invite link, assign and remove admin status of members, change the group description.
- Search for desired content and filter the results by user name, user 'bio', post title, post content, group name and group description.
- Update your profile settings, changing you 'bio' and adding a profile picture.
- Follow and unfollow other users to curate your homepage feed and filter posts by the users you follow.
- Vote on posts by giving a opvote or downvote.

## Getting Started

1. Clone the repository to your local machine.
2. Install the necessary packages using pip:
```
pip install -r requirements.txt
```
3. Initialize the database:
```
python manage.py migrate
```
4. Run the Django server:
```
python manage.py runserver
```
5. Open your web browser and navigate to http://localhost:8000/.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
