from my_token import TOKEN
from telegram.ext import Updater, CommandHandler,Filters, MessageHandler
from command import *

updater = Updater(TOKEN)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', Start),MessageHandler(Filters.text('Старт'), Start)],
    states={
        SELECT: [MessageHandler(Filters.text('Просмотреть записи'), ViewAll),
                 MessageHandler(Filters.text('Добавить'), AddItem),
                 MessageHandler(Filters.text('Изменить'), DataChange),
                 MessageHandler(Filters.text('Фильтр'), ViewFilter),
                 MessageHandler(Filters.text('Удалить'), RemoveItem),
                 MessageHandler(Filters.text('Отдел'), ViewDepartments),
                 MessageHandler(Filters.text('Должность'), ViewPositions)],
        INPUTNAME: [MessageHandler(Filters.text('Отменить'), CancelAdd),MessageHandler(Filters.text, InputName)],
        INTUPBIRTH: [MessageHandler(Filters.text('Отменить'),CancelAdd),MessageHandler(Filters.text, InputBirth)],        
        INPUTTEL: [MessageHandler(Filters.text('Отменить'),CancelAdd),MessageHandler(Filters.text, InputTel)],
        INPUTDEP: [MessageHandler(Filters.text('Отменить'),CancelAdd),MessageHandler(Filters.text, InputDepartment)],
        INPUTPOS: [MessageHandler(Filters.text, InputPosition)],
        SAVE: [MessageHandler(Filters.text('Отменить'), CancelAdd),MessageHandler(Filters.text('Сохранить'), SaveDB)],
        INPUTFILTER: [MessageHandler(Filters.text('Отменить'), CancelAdd),MessageHandler(Filters.text, InputFilter)],
        INPUTID: [MessageHandler(Filters.text('Отменить'), CancelRemove),MessageHandler(Filters.text, InputID)],
        CONFIRMREM: [MessageHandler(Filters.text('Удалить'), ConfirmRemove),MessageHandler(Filters.text('Отменить'), CancelRemove)],
        CANGE: [MessageHandler(Filters.text('Отменить'), CancelAdd),MessageHandler(Filters.text, MenuCange)],
        CANGEID:[MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, CangeID)],
        CANGENAME: [MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, InputNewName)],
        CANGEBIRTH: [MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, InputNewBirth)],        
        CANGETEL: [MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, InputNewTel)],
        CANGEDEP: [MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, InputNewDep)],
        CANGEPOS: [MessageHandler(Filters.text('Отменить'), CancelCange),MessageHandler(Filters.text, InputNewPos)]},
    fallbacks=[MessageHandler(Filters.text('Выход'), Exit)]
    )
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.command, Unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, Text))

print("Бот в работе!")
updater.start_polling()
updater.idle()
