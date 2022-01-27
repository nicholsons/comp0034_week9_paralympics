from paralympics_app.models import User


def test_user_table_has_one_more_row(db, new_user):
    """
        GIVEN the app database
        WHEN a new user is inserted in the User table
        THEN the row count should increase by one
        """
    row_count_1 = User.query.count()
    db.session.add(new_user)
    db.session.commit()
    row_count_2 = User.query.count()
    assert row_count_2 - row_count_1 == 1
