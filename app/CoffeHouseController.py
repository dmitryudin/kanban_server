

@app.route('/coffehouse/edit_pictures')
def coffeHouseEditPicture():
    '''
    получает на вход массив с url изображений
    если url в базе данных не соответсвует переданному, то
    изображение на сервере удаляется, если вместо url передаётся base64 строка,
    то создаётся новое изображение. Метод возвращает новый массив c url картинок
    '''
    d = json.loads(request.get_data().decode('utf-8'))
    coffeHouse = model.CoffeHouse.query.get(int(d['id']))
    # TODO нужно реализовать этот контроллер всё-таки
    return 'Hello World!'
