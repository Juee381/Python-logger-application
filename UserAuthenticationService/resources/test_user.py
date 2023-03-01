def test_register_user(client):
    response = client.post('/register', json={"username": "jui12345",
                                              "password": "Jui12345678"
                                              }, )
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully."}


def test_register_existing_user(client):
    response = client.post('/register', json={"username": "jui12345",
                                              "password": "Jui12345678"
                                              }, )
    assert response.status_code == 409
    assert response.json == {"message": "A user with that username already exists."}


def test_register_user_with_invalid_password(client):
    response = client.post('/register', json={"username": "jui12345",
                                              "password": "Jui"
                                              }, )
    assert response.status_code == 400
    assert response.json == {"message": "Enter a valid password."}


def test_register_user_with_invalid_username(client):
    response = client.post('/register', json={"username": "jui",
                                              "password": "Jui12345678"
                                              }, )
    assert response.status_code == 400
    assert response.json == {"message": "Enter a valid username."}


def test_login_password_not_match(client):
    response = client.post('/login', json={"username": "jui12345",
                                           "password": "Jui"
                                           }, )
    assert response.status_code == 401
    assert response.json == {"message": "Password does not match."}


def test_login_user_not_exist(client):
    response = client.post('/login', json={"username": "abc",
                                           "password": "Jui12345678"
                                           }, )
    assert response.status_code == 401
    assert response.json == {"message": "User does not exists with given username."}
