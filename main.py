import sqlite3


class Db:
    def __init__(self, name):
        self.name = name

    def create_db(self, nom, number, email, tovar, price, dt, errors):
        con = sqlite3.connect(self.name + '.db')

        cur = con.cursor()

        cur.execute('''CREATE TABLE if not exists customer
                    (id integer, auto_increment,
                    nom varchar(50),
                    email varchar(50),
                    tel varchar(20),
                    primary key(id))
                    ''')

        cur.execute('''CREATE TABLE if not exists shoping
                          (id_ integer, auto_increment,
                          tovar varchar(50),
                          price varchar(20),
                          dt varchar(10),
                          customer_name varchar(20),
                          primary key(id_))
                          ''')

        cur.execute('''CREATE TABLE if not exists errors
                          (id_ integer, auto_increment,
                          errors varchar(255),
                          primary key(id_))
                          ''')
        data_tuple = [nom, number, email]
        data_tuple2 = [tovar, price, dt, nom]
        data_tuple3 = [errors]

        q1 = """INSERT INTO customer(nom, tel, email) 
        VALUES (?, ?, ?);"""

        q2 = """INSERT INTO shoping (tovar, price, dt, customer_name)
        VALUES (?, ?, ?, ?);"""

        q3 = """INSERT INTO errors (errors)
                VALUES (?);"""

        cur.execute(q1, data_tuple)

        cur.execute(q2, data_tuple2)

        cur.execute(q3, data_tuple3)

        con.commit()

        con.close()

        return 'Готово!'


def send_mess():
    # Импортирование всех нужних библиотек для работы с уведамление алиф
    import smtplib
    import requests
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from platform import python_version
    import datetime
    # Заполнение глобалних переменних
    global sender, recipients
    subject = 'Хароҷоти шумо'
    nom = input('Введите имя клиента: ')
    number_cust = input('Введите номер телефона клиента например 928483377: ')
    recipients = [input('Введите адресс эл-почты клиента например safaroffqodirjon@gmail.com: ')]
    tovar = input('Введите имя товаров: например телефон, наушники: ').split(',')
    st1 = ''
    for i in tovar:
        st1 += i
        st1 += ", "
    tovar = st1[:-2]
    price = input('Введите стоимость товаров: ')


    info = ''
    errors = []
    print('!!!Внимание только раз в день можно отправлять бесплатный СМС!!!')

    key = input('Что бы отправить эл-почту нажмите 0, а СМС 1: ')

    if str(key) == '0':
        user = input(
            'Введите адресс вашей почты например yagonnafar@gmail.com:\n(рекомендуем вам исползовать тестовый якшик):')

        server = 'smtp.gmail.com'
        password = input('Введите свой пароль эл-почты: ')
        sender = user
        text = '<h1>Асалому алайкум мизоҷи мӯҳтаарам шумо<h1> </b> {} - ро бо нархи <h1 style="color: red">{} сомонӣ</h1><h1 style="color":red>харидори кардед</h1>'.format(
            tovar[::],
            price)

        html = '<html><head></head><body><p>' + text + '</p></body></html>'

        try:
            msg = MIMEMultipart('alternative')

            msg['Subject'] = subject
            msg['From'] = 'Python script <' + sender + '>'
            msg['To'] = ', '.join(recipients)
            msg['Reply-To'] = sender
            msg['Return-Path'] = sender
            msg['X-Mailer'] = 'Python/' + (python_version())

            part_text = MIMEText(text, 'plain')
            part_html = MIMEText(html, 'html')

            msg.attach(part_text)
            msg.attach(part_html)

            mail = smtplib.SMTP_SSL(server)
            try:
                mail.login(user, password)
            except TypeError:
                errors.append('Ошыбака пароля')
            mail.sendmail(sender, recipients, msg.as_string())
            mail.quit()
        except OSError:
            errors.append('Ошыбка с соединением при отпраке email')


    elif str(key) == '1':
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': '+992' + number_cust,
                'message': 'Шумо {} харидед'.format(tovar),
                'key': 'textbelt',
            })

            dct = dict(resp.json())

            # info = "!!!" + str(dct['error']) + "!!! " + info
            if not dct['success']:
                errors.append(str("Толко один бесплатный СМС в день" + " >> " + str(dct['error'])))
        except OSError:
            errors.append('Ошыбка соединения при отправке СМС клиенту {}'.format(nom))




    else:
        print('Введите только числа 0 или 1')
        errors.append('Неправилный ввод в определение канала')

    if len(errors) == 0:
        info += '☻☻☻Все прошло хорошо☺☺☺'
    else:
        st = ''
        for i in errors:
            st+=i
            st += ' '
        info += 'Были ошыбки: ' + st

    dt = datetime.datetime.now()
    db = Db('AlifDataBase')
    db.create_db(nom=str(nom), number=str(number_cust), email=str(recipients),
                 tovar=str(tovar), price=str(price), dt=str(dt), errors=str(errors))
    print()
    print("**********************************************\n")
    return info + "\n!!!Все данные о клиенте и об ошыбках сохранены в базе данных!!!"


print(send_mess())

