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

Пример минимального применения:
```python
# подключение только базового управления
from alice_py_ycf import Alice

# выполняется при первом запуске навыка
@Alice.start()
def start_f(ctx, data):
    return {
        "txt" : 'Это первый запуск приложения',
    }

# выполняется только если придет "Привет" или "Хай"
@Alice.command(['Привет','Хай'])
def comm_f(ctx, data):
    return {
        "txt":'И тебе привет!',
    }

# выполняется если это не первая комада и 
# не подходит ни под один из command( !! )
@Alice.any()
def any_f(ctx, data):
    return {
        "txt":'Неизвестная команда',
        'tts' : 'Эта команда мне неизвестна'
    }

# запуск фреймворка
Alice.run()
```

### Лицензия
----
проект под MIT лицензией


