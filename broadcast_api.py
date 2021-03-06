from mysql import mysql
from mysql import DB_Exception
from datetime import date
from datetime import datetime
from datetime import timedelta
from dataAccessObjects import *
import os.path
import json

def getDisplayContent(sche_target_id,return_msg):
    #get type from target id prefix
    targetIdPrefix = sche_target_id[:4]
    if targetIdPrefix == "imge":
        with ImageDao() as imageDao:
            file_info = imageDao.getIdSysName(Id=sche_target_id)
        return_msg["file_type"] = "image"
    elif targetIdPrefix == "text":
        with TextDao() as textDao:
            file_info = textDao.getIdSysName(Id=sche_target_id)
        return_msg["file_type"] = "text"
    else :
        return_msg["error"] = "target id type error {}".format(targetIdPrefix)
        return return_msg

    try:
        type_id = file_info['typeId']
        system_file_name = file_info['systemName']
        return_msg["like_count"] = file_info['likeCount']
    except:
        return_msg["error"] = "no file record"
        return return_msg

    with DataTypeDao() as dataTypeDao:
        type_dir = dataTypeDao.getTypeDir(typeId=type_id)
        type_name = dataTypeDao.getTypeName(typeId=type_id)
    if type_dir == None or type_name == None:
        return_msg["error"] = "No such type id {}".format(type_id)
        return return_msg

    targetFile = os.path.join("static", type_dir, system_file_name)
    return_msg["file"] = os.path.join(type_dir, system_file_name)
    return_msg["type_name"] = type_name

    #if text read file
    if return_msg["file_type"] == "text":
        if not os.path.isfile(targetFile) :
            return_msg["error"] = "no file"
            return return_msg
        else :
            with open(targetFile,"r") as fp:
                file_content = json.load(fp)
            return_msg["file_text"] = file_content
    return return_msg

#The API load schedule.txt and find out the first image which has not print and the time limit still allow
def load_schedule():
    try:
        return_msg = {}
        return_msg["result"] = "fail"

        #find next schedule
        with ScheduleDao() as scheduleDao:
            next_schedule = scheduleDao.getNextSchedule()
        if next_schedule is None:
            return_msg["error"] = "no schedule"
            return return_msg
        return_msg["schedule_id"] = next_schedule['schedule_id']
        sche_target_id = next_schedule['sche_target_id']
        return_msg["display_time"] = int(next_schedule['display_time'])

        return_msg = getDisplayContent(sche_target_id,return_msg)
        if "error" in return_msg:
            return return_msg

        #update display count
        if return_msg["file_type"] == "image":
            with ImageDao() as imageDao:
                imageDao.addDisplayCount(sche_target_id)
        elif return_msg["file_type"] == "text":
            with TextDao() as textDao:
                textDao.addDisplayCount(sche_target_id)

        return_msg["result"] = "success"
        return return_msg
    except DB_Exception as e:
        return_msg["error"] = e.args[1]
        return return_msg

