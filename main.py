import os
import random

try:
    import telebot
    import img2pdf
    from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
except:
    os.system('pip install pyTelegramBotAPI || pip install img2pdf')
    os.system('cls || clear')

token = str(input("[$] Please Enter Your Bot Token:"))
bot = telebot.TeleBot(token)

adminList = [5289222617]

dictt = {}  # We Will Save All Users Photos & ID Here , Like This : 'id':[photo1, photo2, photo3]

# I Cant Save It In Json File
# Because We Don't Save The Photos Path, We Save The Bytes
# And I Think We Cant Write The Bytes In The Json File,
# Even if you convert it to string and when you read the file convert it to bytes
# it's a complicated thing and makes the code slow, but it's the best!

keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton("تحويل الصور الى PDF", callback_data='convert')
button2 = InlineKeyboardButton("مسح جميع الصور", callback_data='clear')
keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])
def help(message):
    name = message.chat.first_name
    msg = f"""
<b>مرحبًا 👋 {name} إلى بوت تحويل الصور إلى PDF</b>

فقط أرسل الصور وسوف <b>أحولها إلى PDF</b> بالترتيب الذي ترسله 


1. لا توجد <b>خسارة للجودة</b>: ستحتوي الصورة المضمنة في ملف PDF دائمًا على نفس معلومات اللون تمامًا لكل بكسل مثل الصور التي أرسلتها.

2. <b>صغر الصور</b>: إن أمكن، فإن الاختلاف في حجم الملف بين الصورة التي أدخلتها وملف PDF الناتج سيكون فقط عبء حاوية PDF نفسها.

3. <b>السرعة</b>: إن أمكن، يتم لصق صورة الإدخال في مستند PDF كما هي دون الحاجة إلى إعادة تشفير بيانات البكسل المستهلكة للوحدة المعالجة المركزية.

ملاحظة: يمكنك فقط إرسال 20 صورة كحد أقصى.
"""
    bot.send_message(message.chat.id, msg, parse_mode="HTML")


@bot.message_handler(content_types=['photo'])  # If User Sent A Photo This Func Will Run < The Func Will Save The Photo
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    photoBytes = bot.download_file(file_info.file_path)
    try:
        dictt[message.chat.id]
    except KeyError:
        dictt[message.chat.id] = []

    photosList = dictt[message.chat.id]
    if len(photosList) > 19:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text="*تـحـذيـر : لايمكن اضافة المزيد من صور الى قائمتك لانك تعديت العد المسموح - 20 -*",
                              parse_mode="markdown", reply_markup=keyboard)
    else:
        photosList.append(photoBytes)
        bot.reply_to(message,
                     f'* تم اضافة صورة الى قائمة الصور الخاصة بك 🙌*\n\n- عدد الصور التي تم حفظه الى قائمتك : {len(photosList)}',
                     parse_mode="markdown", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  # If The Enter Convert Button Will Convert All Photos In He List
def convert(call):
    global photosList
    if call:
        if call.data == 'convert':
            try:
                photosList = dictt[call.message.chat.id]
                pdf = img2pdf.convert(photosList)
                numebr = random.randint(1, 100)
                with open(f"{numebr}.pdf", "wb") as file:
                    file.write(pdf)
                    file.close()

                with open(f"{numebr}.pdf", "rb") as doc:
                    bot.send_document(call.message.chat.id, doc)
                    doc.close()

                os.remove(f'{numebr}.pdf')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"تم تحويل {len(photosList)} صور الى PDF")
                photosList.clear()
                print(f"Someone Convert He Photos | ID => {call.message.chat.id}")

            except MemoryError or Exception as Error:
                print(f"Error => {Error}\nMean => There Is An Error With Your Memory (RAM) ):")
                print(f"Why => Maybe Because There Is A Lot Of Data (photo) In The Dict (where we save photos)")
                print(
                    "How To Fix => You Dont Need To Do Anything, The Program Will Delete All Data (photos) From The Dict")
                print("To Know More About The Error => https://2u.pw/mmhRDI")
                print(
                    "Ask About Error => https://t.me/arabipython(Telegram Group) Or Ask The Developer on Telegram => rar_99\n")

                dictt.clear()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="*يوجد خطاء في ايجاد الصور الخاصة بك, الرجاء المحاولة مرة اخرى.. 😔*",
                                      parse_mode="markdown")

            except Exception as Error:
                if not Error == call.message.chat.id or not Error == 'Unable to process empty list':
                    print(f"Error => {Error}")
                    print("To Know More About The Error => https://2u.pw/OXGWyi")
                    print(
                        "Ask About Error => https://t.me/arabipython(Telegram Group) Or Ask The Developer on Telegram => rar_99\n")

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="*ليس لديك صور لحذفها 😰, لـ اضافة صور ارسلها لي وسوف احولها بالترتيب الذي ترسله 😁 *",
                                      parse_mode="markdown")

        elif call.data == 'clear':
            try:
                photosList = dictt[call.message.chat.id]
                photosList.clear()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="*- تم مسح جميع الصور التي تم حفظها !*", parse_mode="markdown")
            except KeyError:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="*ليس لديك صور لحذفها 😰, لـ اضافة صور ارسلها لي وسوف احولها بالترتيب الذي ترسله 😁 *",
                                      parse_mode="markdown")

        elif call.data == 'more':
            keyboard3 = InlineKeyboardMarkup()
            button5 = InlineKeyboardButton("شراء قهوة", url='https://www.buymeacoffee.com/rarr')
            button6 = InlineKeyboardButton("تواصل معي", url='https://t.me/rar_99')
            keyboard3.add(button5, button6)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""`عن العضوية المميزة  😁`



1. تحويل عدد لانهائي من الصور 🤯            
2. امكانية تغير اسم الملف  🤩
3. ملف يخزن الصور الخاصة بك ولن ينحذف الا عندما تطلب ذالك 😎        
4. امكانية تحويل الصور الى PDF و تحويل PDF الى صور *بسرعة فائقة*  ⚡ 
5.. التاكد من استمرارية البوت وتطوره 🛠
5. العضوية تستمر معك الى الابد 🙌 
7. العضوية تشمل *البوتات الاخرى* 😨 

            مـاذا تـنـتـظـر . . ؟ !
            """, )


@bot.message_handler(commands=['exit'])
def exitBot(message):
    if int(message.chat.id) in adminList:
        try:
            bot.reply_to(message, text="The Bot Exit Successfully ⚡")
            exit()

        except Exception as ErrorExit:
            bot.reply_to(message, text=f"Error => {ErrorExit}")


@bot.message_handler(commands=['coffee'])
def support(message):
    keyboard2 = InlineKeyboardMarkup()
    button3 = InlineKeyboardButton("شراء قهوة", url='https://www.buymeacoffee.com/rarr')
    button4 = InlineKeyboardButton("مميزات شراء القهوة", callback_data='more')
    keyboard2.add(button3, button4)
    bot.send_message(message.chat.id,
                     text='*اشتري لي قهوة وستحصل على عضوية مميزة ✨ *\n\n`ارسل لي رسالة مع القهوة تحتوي على اسم حسابك 😊`\n\n',
                     parse_mode="markdown", reply_markup=keyboard2)


print("Bot Running..")
bot.infinity_polling()
