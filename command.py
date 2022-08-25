from tkinter import E
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from database import *
import logging
from menu import *

_db = None
_newName = ""
_dateOfBirth =""  
_newTel = ""
_newDepartment = ""
_newPosition = ""
_id = 0
_msg_change="Изменения внесены."

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT, INPUTNAME, INTUPBIRTH, INPUTTEL, INPUTDEP, INPUTPOS,\
INPUTFILTER, INPUTID, CONFIRMREM,SAVE,REMOTE,CANGE,CANGEID,\
CANGENAME,CANGEBIRTH,CANGETEL,CANGEDEP, CANGEPOS = range(18)

def SendMenu(update: Update, context: CallbackContext):
    markup_key = ReplyKeyboardMarkup(keyboard_menu,resize_keyboard=True)
    update.message.reply_text('Выберите действие:',reply_markup=markup_key)
 
def Start(update: Update, context: CallbackContext):
    global _db
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал работу с базой")
    _db = OpenDataBase()
    msg='Здравствуйте!\nМеня зовут Librarian. Я бот, работающий с базой данных.'
    update.message.reply_text(msg)
    SendMenu(update, context)
    return SELECT

def ViewAll(update: Update, context: CallbackContext):
    try:
        global _db
        user = update.message.from_user
        logger.info(f"Пользователь {user.first_name} выбрал просмотр всей базы")
        data = GetAllPersons(_db)
        message = "\n".join(
        [f"{item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}" for item in data])
        update.message.reply_text(message)
        SendMenu(update, context)
    except:
        update.message.reply_text('Отсутствую записи в базе данных.')
    return SELECT

def AddItem(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} выбрал добавление записи")
    markup_key = BtnCancel(update, context)
    update.message.reply_text("Введите имя сотрудника.",reply_markup=markup_key)
    return INPUTNAME

def InputName(update: Update, context: CallbackContext):
    global _newName
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} ввел имя сотрудника '{text}'")
    _newName = text
    markup_key = BtnCancel(update, context)
    update.message.reply_text(
        "Введите дату рождения сотрудника.",reply_markup= markup_key)
    return INTUPBIRTH

def InputBirth(update: Update, context: CallbackContext):
    global _dateOfBirth
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} ввел дату рождения '{text}'")
    _dateOfBirth = text
    markup_key = BtnCancel(update, context)
    update.message.reply_text(
        "Введите телефон сотрудника",reply_markup= markup_key)
    return INPUTTEL

def InputTel(update: Update, context: CallbackContext) -> int:
    global _newTel
    user = update.message.from_user
    text = update.message.text
    logger.info(
        f"Пользователь {user.first_name} ввел телефон сотрудника '{text}'")
    _newTel = text
    markup_key = BtnCancel(update, context)
    update.message.reply_text(
        "Введите название отдела.",reply_markup= markup_key)
    return INPUTDEP

def InputDepartment(update: Update, context: CallbackContext) -> int:
    global _newDepartment
    user = update.message.from_user
    text = update.message.text
    logger.info(
        f"Пользователь {user.first_name} ввел название отдела '{text}'")
    _newDepartment = text
    markup_key = BtnCancel(update, context)
    update.message.reply_text(
        "Введите должность сотрудника.",reply_markup= markup_key)
    return INPUTPOS

def InputPosition(update: Update, context: CallbackContext):
    global _newName, _dateOfBirth,_newTel, _newDepartment, _newPosition, _db
    user = update.message.from_user
    text = update.message.text
    logger.info(
        f"Пользователь {user.first_name} ввел должность сотрудника '{text}'")
    _newPosition = text
    AddPerson(_db, _newName,_dateOfBirth, _newTel, _newDepartment, _newPosition)
    logger.info(
        f"Пользователь {user.first_name} добавил нового сотрудника '{_newName}, {_dateOfBirth},{_newTel}, {_newDepartment}, {_newPosition}'")
    _newName,_dateOfBirth, _newTel, _newDepartment, _newPosition = ("", "", "", "", "")
    SaveAndCancel(update, context)
    return SAVE

def CancelAdd(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        f"Пользователь {user.first_name} отменил добавление новой записи")
    SendMenu(update, context)
    return SELECT

def ViewFilter(update: Update, context: CallbackContext):
    user = update.message.from_user
    markup_key = BtnCancel(update, context)
    logger.info(
        f"Пользователь {user.first_name} выбрал просмотр базы по фильтру")
    update.message.reply_text("Введите строку для фильтрации.",reply_markup= markup_key)
    return INPUTFILTER

def InputFilter(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    markup_key = BtnCancel(update, context)
    logger.info(
        f"Пользователь {user.first_name} ввел строку для фильрации '{text}'")
    data = GetFilterPerson(_db, text)
    if len(data) != 0:
        message = "\n".join([f"{item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}" for item in data])
    else:
        message = "Нет данных, удовледворяющих условию фильтрации."
    update.message.reply_text(message,reply_markup= markup_key)
    return INPUTFILTER

def RemoveItem(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        markup_key = BtnCancel(update, context)
        logger.info(f"Пользователь {user.first_name} выбрал удаление записи")
        View(update,context)
        update.message.reply_text("Введите ID сотрудника для удаления.",reply_markup= markup_key)
        return INPUTID
    except:
        update.message.reply_text("Отсутствуют записи в базе данных")
        return SELECT

def InputID(update: Update, context: CallbackContext):
    global _id
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} ввел ID сотрудника для удаления '{text}'")
    try:
        _id = int(text)
        person = GetPerson(_db, _id)
        if person == None:
            raise
    except:
        markup_key = BtnCancel(update, context)
        update.message.reply_text(
            "Вы ввели не верный ID.\nВведите ID сотрудника для удаления.",reply_markup= markup_key)
        return INPUTID
    update.message.reply_text("Вы хотите удалить запись о сотруднике?\n\n"
                              f"{person[0]}, {person[1]}, {person[2]}, {person[3]}, {person[4]}, {person[5]}")
    DataRemote(update, context)
    return CONFIRMREM

def ConfirmRemove(update: Update, context: CallbackContext):
    global _db, _id
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} подтвердил удаление записи с id = {_id}")
    RemovePerson(_db, _id)
    SaveDB(update, context)
    return SELECT

def CancelRemove(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} отменил удаление записи")
    SendMenu(update, context)
    return SELECT

def ViewDepartments(update: Update, context: CallbackContext):
    global _db
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} выбрал просмотр справочника отделов")
    departments = GetAllDepartments(_db)
    if len(departments) != 0:
        message = "\n".join([f"{item[0]}, {item[1]}" for item in departments])
    else:
        message = "Справочник отделов пуст"
    update.message.reply_text(message)
    SendMenu(update, context)
    return SELECT

def ViewPositions(update: Update, context: CallbackContext):
    global _db
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} выбрал просмотр справочника отделов")
    positions = GetAllPositions(_db)
    if len(positions) != 0:
        message = "\n".join([f"{item[0]}, {item[1]}" for item in positions])
    else:
        message = "Справочник должностей пуст"
    update.message.reply_text(message)
    SendMenu(update, context)
    return SELECT

def SaveDB(update: Update, context: CallbackContext):
    SaveDataBase(_db)
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} сохранил базу")
    SendMenu(update, context)
    return SELECT

def Exit(update: Update, context: CallbackContext):
    user = update.message.from_user
    markup_key = BtnStart(update, context)
    logger.info(f"Пользователь {user.first_name} завершил работу с базой")
    update.message.reply_text("Работа завершена",reply_markup= markup_key)
    return ConversationHandler.END

def Text(update, context):
    user = update.message.from_user
    text_received = update.message.text
    logger.info(
        f"Пользователь {user.first_name} ввел сообщение '{update.message.text}'")

def Unknown(update, context):
    user = update.message.from_user
    logger.info(
        f"Пользователь {user.first_name} ввел не обработанную комаду '{update.message.text}'")
 
def SaveAndCancel(update: Update, context: CallbackContext):
    markup_key = ReplyKeyboardMarkup(keyboard_save_cancel,resize_keyboard=True)
    update.message.reply_text('Подтвердите действие',reply_markup=markup_key)
    
def DataRemote(update: Update, context: CallbackContext):
    markup_key = ReplyKeyboardMarkup(keyboard_del_cancel,resize_keyboard=True)
    update.message.reply_text('Подтвердите действие',reply_markup=markup_key)
    
def DataChange(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        markup_key = BtnCancel(update, context)
        logger.info(f"Пользователь {user.first_name} выбрал изменение записи")
        View(update,context)
        update.message.reply_text("Введите ID:",reply_markup=markup_key)
        return CANGEID
    except:
        update.message.reply_text("Отсутствуют записи в базе данных")
        return SELECT
        

def CangeID(update: Update, context: CallbackContext):
    global _id
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} ввел ID сотрудника для изменения '{text}'")
    try:
        _id = int(text)
        person = GetPerson(_db, _id)
        update.message.reply_text(
            f"{person[0]}, {person[1]}, {person[2]}, {person[3]}, {person[4]}, {person[5]}") 
    except:
        markup_key = BtnCancel(update, context)
        update.message.reply_text(
            "Вы ввели не верный ID.\nВведите ID сотрудника для изменения.",reply_markup= markup_key)
        return CANGEID
    MenuCange(update,context)
    return CANGE
                       
def InputNewName(update: Update, context: CallbackContext):
    global _newName
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} изменил имя сотрудника '{text.lower()}'")
    _newName = update.message.text
    CangeName(_db,_newName,_id)
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(_msg_change,reply_markup= markup_key)
    return CANGE

def InputNewBirth(update: Update, context: CallbackContext):
    global _dateOfBirth
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} изменил дату рождения'{text.lower()}'")
    _dateOfBirth = update.message.text
    CangeBirth(_db,_dateOfBirth,_id)
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(_msg_change,reply_markup= markup_key)
    return CANGE

def InputNewTel(update: Update, context: CallbackContext):
    global _newTel
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} изменил телефон '{text.lower()}'")
    _newTel = update.message.text
    CangeTel(_db,_newTel,_id)
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(_msg_change,reply_markup= markup_key)
    return CANGE

def InputNewDep(update: Update, context: CallbackContext):
    global _newDepartment
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} изменил отдел '{text.lower()}'")
    _newDepartment = update.message.text
    CangeDep(_db,_newDepartment,_id)
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(_msg_change,reply_markup= markup_key)
    return CANGE

def InputNewPos(update: Update, context: CallbackContext):
    global _newPosition
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Пользователь {user.first_name} изменил должность '{text.lower()}'")
    _newPosition = update.message.text
    CangePos(_db,_newPosition,_id)
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(_msg_change,reply_markup= markup_key)
    return CANGE

def View(update: Update, context: CallbackContext):
        global _db
        user = update.message.from_user
        logger.info(f"Пользователь {user.first_name} выбрал просмотр всей базы")
        data = GetAllPersons(_db)
        message = "\n".join([f"{item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}" for item in data])
        update.message.reply_text(f"{message}")

    
def MenuCange(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    try:
        id=int(text)
        if type(id)==int: msg="Для изменения записи нажмите кнопку:"
    except: msg=f'Меняем {text.lower()}'
    if text=="Выйти": msg="Выход"
    logger.info(f"Пользователь {user.first_name} выбрал для изменения '{text.lower()}'")
    markup_key = KeyboardCange(update, context)
    update.message.reply_text(f'{msg}',reply_markup=markup_key)
    match text:
        case "Ф.И.О.": return CANGENAME
        case "Дата рождения": return CANGEBIRTH
        case "Телефон": return CANGETEL
        case "Отдел": return CANGEDEP
        case "Должность": return CANGEPOS
        case "Выйти": 
            SendMenu(update, context)
            return SELECT