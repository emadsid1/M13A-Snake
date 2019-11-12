from json import dumps
from class_defines import User, Mesg, data
from datetime import datetime, timedelta, timezone
from exception import ValueError, AccessError
from helper_functions import * # TODO: change this *

# nom = User("naomizhen@gmail.com", "password", "naomi", "zhen", "nomHandle", "12345", 1)
# ben = User("benkah@gmail.com", "password", "ben", "kah", "benHandle", "1234", 2)
# chan1 = channel("chatime", True, 1, 5)
#
# data = {
#     "accounts": [nom, ben],
#     "channels": [chan1]
# }

def user_profile(token, user_id):
    global data
    valid = False
    user = {}
    for acc in data["accounts"]:
        if token == acc.token: # note: assumes token is valid
            valid = True
            if int(user_id) == int(acc.u_id):
                user["email"] = acc.email
                user["name_first"] = acc.name_first
                user["name_last"] = acc.name_last
                user["handle_str"] = acc.handle
            else:
                raise ValueError(description = f"wrong u_id") # wrong u_id
    if valid == False:
        raise AccessError(description = "invalid token") # invalid token
    return dumps({
    "email": user["email"],
    "name_first": user["name_first"],
    "name_last": user["name_last"],
    "handle_str": user["handle_str"]
    })

def user_profile_setname(token, name_first, name_last):
    global data
    if not(len(name_first) >= 1 and len(name_first) <= 50):
        raise ValueError(description = "ValueError")
    if not(len(name_last) >= 1 and len(name_last) <= 50):
        raise ValueError(description = "ValueError")

    for acc in data["accounts"]:
        if token == acc.token:
            acc.name_first = name_first
            acc.name_last = name_last
        else:
            raise ValueError(description = "invalid token") # invalid token
    return {}


def user_profile_email(token, email):
    global data
    check_email(email)
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if email == acc.email:
            raise ValueError(description = "email already being used") # email already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].email = email
    else:
        raise AccessError(description = "token is invalid") # token is invalid
    return dumps({})

def user_profile_sethandle(token, handle):
    global data
    if len(handle) < 3 or len(handle) > 20:
        raise ValueError(description = "handle has incorrect number of chars") # handle has incorrect number of chars
    counter = 0
    found = False
    for acc in data["accounts"]:
        if token == acc.token:
            found = True
        if handle == acc.handle:
            raise ValueError(description = "handle already being used") # handle already being used
        if found is False:
            counter += 1
    if found is not False:
        data["accounts"][counter].handle = handle
    else:
        raise AccessError(description = "token is invalid") #token is invalid
    return dumps({})

# DOES NOT NEED TO BE COMPLETED UNTIL ITERATION 3
def user_profile_uploadphoto():
    global data
    request = request.get("img_url")
    if request != 200:
        raise ValueError(description = "ValueError")
    url = request.form.get("img_url")
    # how to get image size?
    return dumps({})

def users_all(token):
    global data
    user_list = []
    valid = False
    for acc in data["accounts"]:
        user_list.append(acc.u_id)
        if token == acc.token:
            valid = True
    if valid == False:
        raise AccessError(description = "token is invalid") # token is invalid
    return dumps({'users': user_list})

def standup_start(token, channel, length):
    global data
    ch_num = find_channel(channel) # raises ValueError if channel does not exist
    if data["channels"][ch_num].is_standup == True:
        raise AccessError(description = "AccessError") # standup is already in progress
    if length <= 0:
        raise ValueError(description = "ValueError") # standup length needs to be greater than 0
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel

    # starts standup
    data["channels"][ch_num].is_standup = True
    finish = datetime.now() + timedelta(seconds=length)
    data["channels"][ch_num].standup_time = finish
    standup_finish = finish.replace(tzinfo=timezone.utc).timestamp()
    t = Timer(length, standup_active, (token, channel))
    t.start()

    return dumps({
        "time_finish": standup_finish
    })

def standup_active(token, channel):
    global data
    ch_num = find_channel(channel) # raises AccessError if channel does not exist
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel
    if data["channels"][ch_num].is_standup == False:
        finish = None
    else:
        if data["channels"][ch_num].standup_time < datetime.now():
            data["channels"][ch_num].is_standup = False
            standup_end() # TODO: write this function
        else:
            finish = data["channels"][ch_num].standup_time
    return dumps({
        "is_active": data["channels"][ch_num].is_standup,
        "time_finish": finish
    })

def standup_send(token, channel, message):
    global data
    ch_num = find_channel(channel) # raises AccessError if channel does not exist
    if data["channels"][ch_num].is_standup == False:
        raise ValueError(description = "ValueError") # standup is not happening atm
    if len(message) > 1000:
        raise ValueError(description = "ValueError") # message too long
    check_in_channel(token, ch_num) # raises AccessError if user is not in channel

    # TODO: how to check if standup has finished?
    data["channels"][ch_num].standup_messages.append(message)
    return dumps({})

def search(token, query_str):
    global data
    for acc in data["accounts"]:
        if token == acc.token:
            ch_list = acc.in_channel
    messages = []
    for ch in ch_list: # assume in_channel object is list of channel classes
        for msg in ch.messages:
            if query_str in msg.message:
                messages.append({
                    "message_id": msg.message_id,
                    "u_id": msg.sender.user_id,
                    "message": msg.message,
                    "time_created": msg.create_time,
                    "reacts": msg.reaction,
                    "is_pinned": msg.pin
                })

    return dumps({messages})

def admin_userpermission_change(token, u_id, p_id):
    global data
    if not(perm_owner < p_id or p_id < perm_member):
        raise ValueError(description = 'permission_id does not refer to a value permission') # invalid perm_id
    for acc in data['accounts']:
        if acc.token == token:
            if not(acc.perm_id >= p_id):    # does not have permission to change p_id
                raise AccessError(description = 'The authorised user is not an admin or owner')
    for acc in data['accounts']:
        if acc.user_id == u_id:
            acc.perm_id = p_id
            if p_id == perm_member:
                for chan in data['channels']:
                    if u_id in chan.owners:
                        if len(channel.owners) != 1:
                            chan.owners.remove(u_id)
                    if not(u_id in chan.members):
                        chan.members.append(u_id)
            else:
                for chan in data['channels']:
                    if u_id in chan.members:
                        chan.members.remove(u_id)
                    if not(u_id in chan.owners):
                        chan.owners.append(u_id)
            return {}
    raise ValueError('u_id does not refer to a valid user')

# if __name__ == '__main__':
#     app.run(debug=True)
