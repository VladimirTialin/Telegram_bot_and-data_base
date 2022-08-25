from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from database import *
from menu import *
#  Кнопки
keyboard_cange = [['Ф.И.О.', 'Дата рождения', 'Телефон'],['Отдел','Должность','Выйти']]
keyboard_menu = [['Добавить', 'Изменить', 'Удалить'],['Фильтр','Отдел','Должность'],['Просмотреть записи','Выход']]
keyboard_start=[['Старт']]
keyboard_cancel=[['Отменить']]
keyboard_save_cancel = [['Сохранить', 'Отменить']]
keyboard_del_cancel = [['Удалить', 'Отменить']]

def KeyboardCange(update: Update, context: CallbackContext):
    global keyboard_cange
    return ReplyKeyboardMarkup(keyboard_cange, one_time_keyboard=True,resize_keyboard=True)

def BtnCancel(update, context):   
    return ReplyKeyboardMarkup(keyboard_cancel, one_time_keyboard=True,resize_keyboard=True)

def BtnStart(update: Update, context: CallbackContext):
    return ReplyKeyboardMarkup(keyboard_start, one_time_keyboard=True,resize_keyboard=True)