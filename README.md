# alice-py-ycf 
## <font color='#6839CF'>Alice</font>-<font color='#6839CF'>Py</font>thon-<font color='#6839CF'>Y</font>andex<font color='#6839CF'>C</font>loud<font color='#6839CF'>F</font>unction
> v 0.1
>
> Python >= v 3.8
> 

Фреймворк для разработки навыков Яндекс Алисы на Python

> Адаптирован для работы с Yandex Cloud Function
 
- Минималистичен
- Нет внешних зависимостей
- Достаточно базового уровня Python

----
_Важные ссылки:_
- [Управление навыками Алисы](https://dialogs.yandex.ru/developer)
- [Документация разработчика Алисы](https://yandex.ru/dev/dialogs/alice/doc/ru/)
- [Размещение навыка в Yandex Cloud](https://yandex.ru/dev/dialogs/alice/doc/ru/deploy-ycloud-function)
---

Пример возможностей.<br>Файл index.py с функцией handler для Yandex Function Cloud:
```python
def handler(event, context):
    # подключение только базового управления
    from alice_py_ycf import Alice, AddScene

    # создание еще одной сцены
    Alice.red_room = AddScene()

    # выполняется при первом запуске навыка 
    @Alice.start()
    def start_f(ctx, data):
        return {
            "txt" : 'Это первый запуск приложения',
        }

    # выполняется в основной комнате только если придет "привет" или "хай"
    @Alice.command(['привет','хай'])
    def comm_f(ctx, data):
        return {
            "txt":'И тебе привет!',
        }

    @Alice.command(['хочу в красную комнату','пошли в красную комнату'])
    def comm_f(ctx, data):
        data['scene'] = 'red_room'
        return {
            "txt": 'Отлично! Переходим в красную комнату',
            'data': data
        }

    # выполняется в основной комнате если это не первый запуск и 
    # не подходит ни под один из command( !! )
    @Alice.any()
    def any_f(ctx, data):
        return {
            "txt": 'Неизвестная команда',
            'tts': 'Эта команда мне неизвестна'
        }

    # выполняется в дополнительной комнате (red_room) если 
    # пользователь находится в ней и 
    # не подходит ни под один из command( !! ) из этой комнаты
    @Alice.red_room.any()
    def any_f(ctx, data):
        return {
            "txt": 'Неизвестная команда',
            'tts': 'Эта команда мне неизвестна',
            'data':data
        }
    # выполняется в только в дополнительной комнате (red_room) 
    # если пользователь в ней и не одна команда 
    # не подходит ни под один из command( !! ) из этой комнаты
    @Alice.red_room.command(['привет','хай'])
    def any_f(ctx, data):
        return {
            "txt": 'И тебе привет из красной комнаты',
            'tts': 'И тебе прив+ет из кр+асной комнаты',
            'data':data
        }
    
    # команда для возврата в основную комнату
    @Alice.red_room.command(['обратно в основной комнату','назад'])
    def any_f(ctx, data):
        data['scene'] = ''
        return {
            "txt": 'И тебе привет из красной комнаты',
            'tts': 'И тебе прив+ет из кр+асной комнаты',
            'data': data
        }
    
    # выполняется за пределами установленного таймаута
    @Alice.timeout()
    def any_f(ctx, data):
        return {
            "txt": 'Что-то пошло не так..',
            'data':data
        }

    # работа фреймворка
    # установлен timeout 4сек, за пределами которого 
    # будет отправлено 
    # подготовленное сообщение. 
    # default timeout = 3сек.
    return Alice.run(event, timeout=4)
```
**Особенности работы с фреймворком:**
 
- В любом ответе, значение "txt" обязателено: <br>
return {<br>
            <font color='red'>"txt":</font> 'текст ответа',<br>
            ( ... )

- Значение "tts" не является обязательным и может отсутствовать. В этом случае подставляется значение из "txt".

- Значение "txt" можно передавать массивом:
```python
choice_response = [
    {'txt':'первый вариант'}
    {'txt':'вариант посложней',
    'tts': 'вариант посложн+ей'},
    {'txt':'третий вариант ответа'}
]
@Alice.any()
    def any_f(ctx, data):
        return {
            "txt":choice_response,
        }
```
Из массива будет взят один случайный вариант ответа.

- Если навык не сможет ответить за отведенное время, можно ответить пользователю подготовленным ответом. 
```python
# (...)

# ответ который последует если навык выйдет за пределы timeout`а
@Alice.timeout()
    def any_f(ctx, data):
        return {
            "txt": 'Что-то пошло не так, но мы обязательно разберемся.. Давай попробуем еще раз.',
        }

    # не обязательный параметр timeout = количество секунд, через которые последует подготовленный ответ
    return Alice.run(event, timeout=4)
```

<font color="#67CDFE">ctx</font> - контекст вызова. Хранит полный полученный json.<br>
<font color="#67CDFE">data</font> - хранит данные сессий и данные сцены (комнат)<br>
```python
data = {
    # название сцены. Пустая строка = основная комната
    'scene': '',

    # хранение состояния сессии
    'us': {},

    # хранение состояния между сессиями
    'ws': {},

    # хранение состояние для экземпляра приложения
    'as': {}

}
```
[Подробнее о состояниях](https://yandex.ru/dev/dialogs/alice/doc/ru/session-persistence)<br>

Переданные данные из json в этой переменной дублируются для быстрого доступа к ним

Изменения в <font color="#67CDFE">data</font> добавляются в отправляемый json если это явно добавлено в <font color="#C3602C">return</font>.

Из всех комнат, кроме основной, передача <font color="#67CDFE">data</font> является обязательной.

--- 

### Лицензия
----
проект под MIT лицензией


