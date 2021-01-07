import datetime
import os
import inspect

def log_message(log_level,global_log_level,message):
    called_func = inspect.currentframe().f_back.f_back.f_code.co_name
    timestamp = str(datetime.datetime.now())[:-4]
    
    if log_level == global_log_level:
        message = timestamp + ' [ ' + called_func + ' ] ' + log_level + ' : ' + message
    else:
        message = None
    return message

def log_writer(log_path,message,filename):
    with open(log_path+filename,'a+') as log_file:
        if message:
            log_file.write(message+'\n')

def log_generate(log_level,global_log_level,message,log_path,filename):
    message_str = log_message(log_level,global_log_level,message)
    log_writer(log_path,message_str,filename)

def get_filename():
    return ('log_'+str(datetime.datetime.now())[:-4]).replace(':','').replace(' ','_')