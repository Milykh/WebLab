from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app


@app.route('/')
def index():
    return render_template('index.html', delete_footer=True)


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))

    if 'username' in request.cookies:
        pass
    else:
        resp.set_cookie('username','some name')

    
    return resp
    


@app.route('/form', methods=['GET','POST'])
def form():
    return render_template('form.html')


@app.route('/phone', methods=['GET','POST'])
def phone():
    if request.method == 'POST':
        errors, form_phone = phone_validator(request.form.getlist('phone')[0]) # 
        return render_template('phone.html', errors=errors, form_phone=form_phone)
    return render_template('phone.html')


def phone_validator(phone):
    if not phone:
        return ['Пустой запрос']
    errors = []
    form_phone = phone
    phone = phone.replace(' ', '')# убираем все лишнее
    phone = phone.replace('(', '')
    phone = phone.replace(')', '')
    phone = phone.replace('-', '')
    phone = phone.replace('.', '')
    if len(phone) >= 2 and phone[0] == '+' and phone[1] == '7':# если длинна боьше 2 и первый + а второй 7
        phone = '8' + phone[2:]# формируем с 8
    if (phone[0] == '8' and len(phone) != 11) or (phone[0] != '8' and len(phone) != 10):# bпроверка на кол цифр
        errors.append('Недопустимый ввод. Неверное количество цифр')
    if len(phone) == 10:# если длина 10
        phone = '8' + phone # доб впереди 8
    for i in phone:
        if not (i >= '0' and i <= '9'):# пошла проверка что все от 0-9
            errors.append('Недопустимый ввод. В номере телефона встречаются недопустимые символы')
            break
    if len(errors) == 0:# если ошибки не случилось формируем правильный вывод символов номера
        form_phone = f'8-{phone[1:4]}-{phone[4:7]}-{phone[7:9]}-{phone[9:]}'
    return errors, form_phone # возвращаем ошибки и номер


if __name__ == "__main__":
    app.run()
