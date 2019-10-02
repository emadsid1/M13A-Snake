from Error import AccessError
import pytest

def auth_login_test():
    # TODO (Fucking apparently we just assume whether the password and email are right or not, and the returned tokens are whatever we want) PLEASE double check tho
    # TODO check if right BUT u_id is some sort of integer and token is a string
    assert auth_login('z5555555@student.unsw.edu.au', 'right password') == (12345, 'correct token')
    with pytest.raises(Exception): # Following should raise exceptions
        assert auth_login('bad email', 'right password')
        assert auth_login('z5555555@asdfghjkl', 'right password')
        assert auth_login('z55555@.com', 'right password')
        assert auth_login('@', 'right password')
        assert auth_login('.com', 'right password')
        assert auth_login('z5555555@student.unsw.edu.au', 'wrong password')
        assert auth_login('z5555555@asdfghjkl', 'wrong password')

def auth_logout_test():
    # TODO if no output how to test?

def auth_register_test():
    assert auth_register('jeffrey.oh@student.unsw.edu.au', 'right password', 'Jeffrey', 'Oh') == ('12345', 'correct token')
    with pytest.raises(Exception): # Following should raise exceptions
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good password', 'Jeffrey', 'This is a string that is much longer than the max length')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'good password', 'This is a string that is much longer than the max length', 'Oh')
        assert auth_register('jeffrey.oh@student.unsw.edu.au', 'password that does not meet requirements', 'Jeffrey', 'Oh')
        assert auth_register('bad email', 'good password', 'Jeffrey', 'Oh')

def auth_passwordreset_request_test():
    # TODO if no output how to test?

def auth_passwordreset_reset_test():
    # TODO if no output how to test?

def channel_invite_test():
    # TODO if no output how to test?

def channel_details_test():
    assert channel_details('valid token', 12345) == ('Jeffrey', ????????) # TODO not sure what the members data type is

def channel_messages_test():
    # TODO not sure what the messages data type is

def channel_leave_test():
    # TODO not sure what the messages data type is

def channel_join_test():
    # TODO not sure what the messages data type is

def channel_addowner_test():
    # TODO not sure what the messages data type is

def channel_removeowner_test():
    # TODO not sure what the messages data type is

def channels_list_test ():
    # TODO yo wtf are these fucking data types

def channels_listall_test():
    # TODO yo wtf are these fucking data types

def channels_create_test()
    assert channels_create('valid token', 'Jeffrey', True) == 12345
    with pytest.raises(Exception): # Following should raise exceptions
        assert channels_create('valid token', 'This is a string that is much longer than the max length', True)