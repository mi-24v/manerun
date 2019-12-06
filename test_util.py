import pytest

import util

@pytest.fixture(scope="module")
def user():
    from model.user import User
    return User("c4bb79b6-65c6-48d3-9f8c-3d979011822d",
        "24d5a63e-ad03-4468-8a97-7bc5a198d594",
        user_token="2vhlQW68aDPlyiuHJ0ff_sample",
        name="baggy-crimson-newfoundland",
        score=50)

@pytest.fixture()
def csv():
    return open("test.csv","r")
    pass

def test_get_user(user):
    assert util.get_user(user.id) == user

def test_get_user_from_token(user):
    assert util.get_user_from_token(user.user_token) == user

def test_get_user_with_token(user):
    assert util.get_user_with_token(user.id, user.user_token) == user

def test_create_user():
    util.create_user()

def test_get_ranking_data():
    util.get_ranking_data()

def test_save_csv(csv, user):
    assert util.save_csv(csv) == user.csv_id

