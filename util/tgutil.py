from telegram import User,Message
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

def get_user_link(from_user:User) -> str:
    return f"[{escape_markdown(from_user.first_name,2)}](tg://user?id={from_user.id})"

def delete_reply_msg(context : CallbackContext):
    msg=context.job.context
    context.bot.delete_message(msg.chat.id,msg.message_id)

def delay_del_msg(context : CallbackContext , msg : Message, delay : int):
    context.job_queue.run_once(delete_reply_msg,delay,context=msg,name=f"delete_msg_{msg.message_id}")

def get_group_info(group_content):
    return f"[{escape_markdown(group_content.title,2)}](https://t.me/c/{str(group_content.id)[4:]})"

def split_msg(msg):
    msg_list = []
    msg_index = len(msg)%4096
    for i in range(msg_index):
        if i < msg_index:
            msg_list.append(msg[4096*i:4096*(i+1)])
    msg_list.append(msg[4096*msg_index:-1])
    return msg_list
