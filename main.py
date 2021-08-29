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
                          cust_id integer,
                          foreign key (cust_id) references customer(id)
                          primary key(id_))
                          ''')

        cur.execute('''CREATE TABLE if not exists errors
                          (id_ integer, auto_increment,
                          errors varchar(255),
                          primary key(id_))
                          ''')
        data_tuple = [nom, number, email]
        data_tuple2 = [tovar, price, dt]
        data_tuple3 = [errors]

        q1 = """INSERT INTO customer(nom, tel, email) 
        VALUES (?, ?, ?);"""

        q2 = """INSERT INTO shoping (tovar, price, dt)
        VALUES (?, ?, ?);"""

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
    subject = 'ВАШ РАСХОД'
    nom = input('Введите имя клиента: ')
    tovar = input('Введите имя товараов: например телефон, наушники: ').split(',')
    price = input('Введите стоимост товаров: ')
    number_cust = input('Введите номр телефона клиента например 928483377: ')
    recipients = [input('Введите адресс эл-почты клиента например safaroffqodirjon@gmail.com: ')]

    user = input(
        'Введите адресс вашей почты например yagonnafar@gmail.com: \n (рекомендуем вам исползовать тестовый почтовый якшик: ')
    info = ''
    errors = []
    print('!!!Бепул фиристонидани СMC дар 1 руз 1 бор мумкин аст!!!')

    key = input('Что бы отправть эл-почту нажмите 0, а СМС 1: ')

    if str(key) == '0':
        server = 'smtp.gmail.com'
        password = input('Введите свой пароль эл-почты: ')
        sender = user
        text = '<h1>Асалому алайкум мизоҷи муҳтаарам шумо<h1> </b> {} - ро бо нархи <h1 style="color: red">{} сомонӣ</h1><h1 style="color":red>харидори кардед</h1>'.format(
            tovar,
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
            mail.login(user, password)
            mail.sendmail(sender, recipients, msg.as_string())
            mail.quit()
        except OSError:
            errors.append('Ошыбка с соединением при отпраке emil')


    elif str(key) == '1':
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': '+992' + number_cust,
                'message': 'Шумо {} харидед'.format(tovar),
                'key': 'textbelt',
            })

            info = str(resp.json()) + " " + info
        except OSError:
            errors.append('Ошибка соединения при отправке СМС клиенту {}'.format(nom))



    else:
        print('Танҳо 0 ва 1 дохил кунед')
        errors.append('Неправилный ввод в определение канала')

    if len(errors) == 0:
        info += '☻☻☻Все прошло хорошо☺☺☺'
    else:
        info += 'Были ошибки: ' + str(errors)

    dt = datetime.datetime.now()
    db = Db('alifdb')
    db.create_db(nom=str(nom), number=str(number_cust), email=str(recipients),
                 tovar=str(tovar), price=str(price), dt=str(dt), errors=str(errors))

    return info + "\n !!!все данные о клиенте и об ошыбках сохранены в базе данных!!!"


print(send_mess())
