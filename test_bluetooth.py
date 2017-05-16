from server_api import *
from mysql import mysql

def test_app_registeration():
    user_data = {
        "bluetooth_id" : "123123123123",
        "nickName" : "John",
        "birthday" : "2017-05-03",
        "occupation" : "bachelor",
        "user_preference" : ["inside","techOrange"]
    }
    print(add_account_and_prefer(user_data))
    print('register finish')

def check_bluetooth_interact():
    db = mysql()
    db.connect()
    assert check_bluetooth_mode_available() == 1
    user_id = find_user_by_bluetooth(db, "123123123123")
    assert user_id != 0
    prefer_data_type = load_now_user_prefer(db, user_id)
    assert prefer_data_type != -1
    receive_result = insert_customized_schedule(user_id, prefer_data_type)
    assert receive_result != -1

def clean_up():
    db = mysql()
    db.connect()
    print(db.cmd('delete from user where user_bluetooth_id = "123123123123"'))

clean_up()
test_app_registeration()
check_bluetooth_interact()
clean_up()
