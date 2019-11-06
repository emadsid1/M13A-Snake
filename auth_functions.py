import jwt
from json import dumps
from uuid import uuid4
from flask import Flask, request
from flask_mail import Mail, Message
from class_defines import data, User
from helper_functions import check_email

def auth_login(email, password):
    global data
    valid = False
    i = 0
    check_email(email)
    for counter, acc in enumerate(data['accounts']):
        if acc.email == email and acc.password == password:
                i = counter
                valid = True
    if (not(valid)):
        raise ValueError('email and/or password does not match any account')
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    data['accounts'][i].token = token.decode('utf-8')
    return dumps({'u_id': data['accounts'][i].u_id, 'token': token.decode('utf-8')})

def auth_logout(token):
    if token == '':
        return dumps({'is_success': False})
    for acc in data['accounts']:
        if token == acc.token:
            acc.token = ''
            return dumps({'is_success': True})
    return dumps({'is_success': False})

def auth_register(email, password, first, last):
    global data
    global account_count

    check_email(email)

    if (len(password) < 6): # if password is too short
        raise ValueError('password is too short (min length of 6)')

    if (not(1 <= len(first) and len(first) <= 50)): # if name is not between 1 and 50 characters long
        raise ValueError('first name must be between 1 and 50 characters long')

    if (not(1 <= len(last) and len(last) <= 50)):   # if name is not between 1 and 50 characters long
        raise ValueError('last name must be between 1 and 50 characters long')

    handle = first + last
    if len(handle) > 20:
        handle = handle[:20]
    curr = 0
    new = 0
    for acc in data['accounts']:
        if acc.email == email:  # if email is already registered
            raise ValueError('email already matches an existing account')
        if acc.handle.startswith(first + last): # confirm handle is unique
            if handle == first + last:
                handle += '0'
            else:
                new = int(acc.handle.split(first + last)[1]) + 1
                if curr <= new:
                    handle = first + last + str(new)
                    curr = new
        elif handle == (first + last)[:20]:
            handle += '0'
    if len(handle) > 20:
        handle = hex(account_count)
        account_count += 1
    handle.lower()
    token = jwt.encode({'email': email}, password, algorithm = 'HS256')
    user_id = int(uuid4())
    data['accounts'].append(User(email, password, first, last, handle, token.decode('utf-8'), user_id))
    return dumps({'u_id': user_id,'token': token.decode('utf-8')})

def reset_request(app, email):
    for acc in data['accounts']:
        if acc.email == email:
            mail = Mail(app)
            resetcode = str(uuid4())
            msg = Message("RESETCODE!",
                sender="snakeflask3@gmail.com",
                recipients=[email])
            msg.body = "Please use this reset code to reset your password: " +'(' + resetcode + ')'
            mail.send(msg)
            acc.reset_code = resetcode
    return dumps({})

def reset_reset(code, password):
    for acc in data['accounts']:
        if code == acc.reset_code:
            if len(password) >= 6:
                acc.password = password
                acc.reset_code = ''
                acc.token = ''
                return dumps({})
            else:
                raise ValueError('password is too short (min length of 6)')
    raise ValueError('reset code is not valid')
