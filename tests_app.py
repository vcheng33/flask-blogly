from unittest import TestCase
from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase (TestCase):
    """ Tests routes for App """

    def setUp(self):
        """ Add sample user"""

        User.query.delete()
        user = User(first_name="Tweety", last_name="Bird", image_url="")
        user2 = User(first_name="Daffy", last_name="Duck", image_url="")
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()

    def test_show_list(self):
        """ Test list shows """

        with app.test_client() as client:

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("a href='/users/", html)
            self.assertIn("Tweety Bird", html)

    
    def test_add_new_user(self):
        """ Test that a new user is added to the database """

        with app.test_client() as client:

            new_user = {"first-name": "Bugs", "last-name": "Bunny", "image-url": "/static/bugs-bunny-test.png"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>Bugs Bunny</li>", html)

    def test_show_edit_user(self):
        """ Test that the edit user form appears """
        
        with app.test_client() as client:

            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("value='Tweety'", html)
            self.assertIn("value='Bird'", html)
            self.assertIn(f"<form action='/users/{self.user_id}/edit'", html)


    def test_edit_user(self):
        """ Test that an user's information is edited in the database """

        with app.test_client() as client:

            edited_info = {
                "first-name": "Tweety", 
                "last-name": "Bird Jr", 
                "image-url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/02/Tweety.svg/320px-Tweety.svg.png"}
            resp = client.post(f"/users/{self.user_id}/edit", data=edited_info, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>Tweety Bird Jr</li>", html)
    

    def test_remove_user(self):
        """ Test that an user is deleted from the database """

        with app.test_client() as client:

            resp = client.post(f"/users/{self.user_id}/delete",follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>Daffy Duck</li>", html)
            self.assertNotIn("<li>Tweety Bird</li>", html)
    

    