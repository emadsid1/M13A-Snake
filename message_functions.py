from flask import Flask, request
from datetime import datetime, timezone
from uuid import uuid4
from json import dumps
from Error import AccessError
from class_defines import *
from helper_functions import *

def send_later():
    global data
    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    sent_stamp = int(request.form.get('time_sent'))
    # get the actual datetime object from a integer stamp input
    dt_sent = datetime.fromtimestamp(sent_stamp)
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    elif dt_sent < datetime.now():
        raise ValueError('Time sent is a value in the past!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # check if the sender has joined the channel
        has_joined = False
        for chan in sender.in_channel:
            if find_channel(chan) == current_channel:
                has_joined == True
        if has_joined == False:
            raise AccessError('You have not joined this channel yet, join first!')
        # generate a globally unique id
        msg_id = int(uuid4())
        while 1:                                    # TODO not sure if this is right
            if datetime.now() == dt_sent:
                break
        # time sent reached and no exceptions raised, send the message
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, chan_id, True))
    return dumps({
        'message_id': msg_id,    
    })
    
def mesg_send():
    global data

    # TESTING
    # data['accounts'].append(user('email', 'password', 'first', 'last', 'handle', 'token', 12345))
    # data['channels'].append(channel('kenny channel', True, 123456, 15))
    # TESTING

    sending_time = datetime.now()
    token = request.form.get('token')
    msg = request.form.get('message')
    chan_id = int(request.form.get('channel_id'))
    if len(msg) > 1000:
        raise ValueError('Message is more than 1000 words!')
    else:
        sender = user_from_token(token)
        current_channel = find_channel(chan_id)
        # generate a globally unique id
        msg_id = int(uuid4())
        # no exceptions raised, then add(send) the message to the current channel
        current_channel.messages.append(mesg(sender, sending_time, msg, msg_id, chan_id, False))
    return dumps({
        'message_id': msg_id,
    })

def mesg_remove():  # TODO no channel id???????
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    remover = user_from_token(token)
    found_msg = find_msg(msg_id)
    # find the channel where the message belongs to
    msg_channel = find_channel(found_msg.in_channel)
    if found_msg.sender != remover:
        raise AccessError('You do not have the permission to delete this message as you are not the sender!')
    elif (check_owner(msg_channel, remover.u_id) == False) or (check_admin(msg_channel, remover.u_id) == False):
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # no exception raised, then remove the message
    msg_channel.messages.remove(found_msg)
    return dumps({

    })

def mesg_edit():
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    new_message = request.form.get('message')
    editor = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if len(new_message) > 1000:
        raise ValueError('Message is more than 1000 words!')
    elif found_msg.sender != editor:
        raise AccessError('You do not have the permission to edit this message as you are not the sender!')
    elif (check_owner(msg_channel, editor.u_id) == False) or (check_admin(msg_channel, editor.u_id) == False):
        raise AccessError('You do not have the permission as you are not the owner or admin of this channel!')
    # edit the message if no exceptions raiseds
    found_msg.message = new_message
    return dumps({
        
    })
    
def mesg_react():
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    reacter = user_from_token(token)
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction != None:
        raise ValueError('This message already contains an active React!')
    # give the message a reaction if no exceptions raised
    found_msg.reaction = reacts(reacter, react_id)
    return dumps({

    })

def mesg_unreact():
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    found_msg = find_msg(msg_id)
    if react_id != 1:
        raise ValueError('Invalid React ID!')
    elif found_msg.reaction == None:
        raise ValueError('This message does not contain an active React!')
    # unreact the message if no exceptions raised
    found_msg.reaction = None
    return dumps({

    })

def mesg_pin():
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    pinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, pinner.u_id) == False:
        raise ValueError('You can not pin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == True:
        raise ValueError('The message is already pinned!')
    elif check_member(msg_channel, pinner.u_id) == False:
        raise AccessError('You can not pin the message as you are not a member of the channel')
    # pin the message if no exceptions raised
    found_msg.is_pinned = True
    return dumps({
        
    })
    
def mesg_unpin():
    global data

    # TESTING
    # user1 = user('email', 'password', 'first', 'last', 'handle', 'token', 1111)
    # channel1 = channel('kenny channel', True, 123456, 15)
    # data['accounts'].append(user1)
    # data['channels'].append(channel1)
    # data['channels'][0].owners.append(user1.u_id)
    # data['channels'][0].admins.append(user1.u_id)
    # data['channels'][0].members.append(user1.u_id)
    # data['channels'][0].messages.append(mesg(user1, datetime.now(), 'hello world', 54321, 123456, False))
    # TESTING

    token = request.form.get('token')
    msg_id = int(request.form.get('message_id'))
    unpinner = user_from_token(token)
    found_msg = find_msg(msg_id)
    msg_channel = find_channel(found_msg.in_channel)
    if check_admin(msg_channel, unpinner.u_id) == False:
        raise ValueError('You can not unpin the message as you are not an Admin of the channel')
    elif found_msg.is_pinned == False:
        raise ValueError('The message is already unpinned!')
    elif check_member(msg_channel, unpinner.u_id) == False:
        raise AccessError('You can not unpin the message as you are not a member of the channel')
    # unpin the message if no exceptions raised
    found_msg.is_pinned = False
    return dumps({
        
    })

if __name__ == '__main__':
    app.run(debug=True)
