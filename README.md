# [Book exchange web service](https://smalllib.herokuapp.com/)

## Introduction
We are sure that many of us like to feel the book in our hands. No matter how they say, an e-book cannot be compared with a regular book.
This is a web service that allows you to share books with other users. Exchange, find those books that will be of interest to you.

## Tech
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Flask-Sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

## Installation

Склонируйте этот репозиторий
```commandline
 git clone https://github.com/<your-username>/book-exchange-social-network.git
```
Установите зависимости
```commandline
pip install -r requirements.txt
```

Запустите проект
```commandline
python -m pytest
```

## Start App

```commandline
python app.py runserver
```
## Start Test
```comandline
python app.py
```

## Contributing

Если вы хотите внести свой вклад в этот проект, пожалуйста, следуйте этим инструкциям:

- Форкните этот репозиторий.
- Создайте ветку для своих изменений.
- Сделайте свои изменения и закоммитьте их.
- Создайте пулл-реквест для объединения ваших изменений с мастер-веткой.

## License
Этот проект лицензирован по лицензии MIT. Для получения дополнительной
информации обратитесь к файлу LICENSE.


Профиль пользователя: Каждый пользователь должен иметь свой профиль, 
в котором отображаются информация о нем, включая историю его обменов, 
коллекцию книг и отзывы других пользователей.

Каталог книг: Пользователи должны иметь возможность добавлять книги в 
свой каталог и просматривать книги, добавленные другими пользователями.

Обмен книгами: Пользователи должны иметь возможность отправлять запросы
на обмен книгами с другими пользователями. Обмен может быть подтвержден
или отклонен другим пользователем.

Уведомления: Пользователи должны получать уведомления о подтвержденных
или отклоненных запросах на обмен, а также о новых запросах и сообщениях
от других пользователей.

Рейтинг пользователей: Можно реализовать систему рейтинга для пользователей,
основанную на их истории обменов и отзывах других пользователей.

Поиск книг: Пользователи должны иметь возможность искать книги по автору,
названию и жанру.

Отзывы о книгах: Пользователи должны иметь возможность оставлять отзывы о
книгах, которые они читали, чтобы другие пользователи могли узнать больше
о книге.