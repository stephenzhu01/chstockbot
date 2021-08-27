from telegram import User,Message
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

def get_user_link(from_user:User) -> str:
    """
    基于telegram.User类，返回用户的链接
    """
    return f"[{escape_markdown(from_user.first_name,2)}](tg://user?id={from_user.id})"

def get_group_info(group_content) -> str:
    """
    基于telegram.Group类，返回群组的信息
    """
    return f"[{escape_markdown(group_content.title,2)}](https://t.me/c/{str(group_content.id)[4:]})"

def delete_reply_msg(context : CallbackContext):
    msg=context.job.context
    context.bot.delete_message(msg.chat.id,msg.message_id)

def delay_del_msg(context : CallbackContext , msg : Message, delay : int):
    """
    设置一个延时删除消息的任务，这个任务就是设置指定的delay秒去调用delet_reply_msg函数
    """
    context.job_queue.run_once(delete_reply_msg,delay,context=msg,name=f"delete_msg_{msg.message_id}")

def split_msg(msg:str) -> list:
    """
    将一个大于4096的消息分割成多个消息
    """
    msg_list = []
    msg_index = len(msg)%4096
    for i in range(msg_index):
        if i < msg_index:
            msg_list.append(msg[4096*i:4096*(i+1)])
    msg_list.append(msg[4096*msg_index:-1])
    return msg_list
