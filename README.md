# api_final
## Описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.   
Произведения делятся на категории, а также им может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).  
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
Пользователи могут оставлять комментарии к отзывам.


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/YablokovaIrina/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов к API:

#### Ресурс auth:
Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

#### Ресурс users:
Получение списка всех пользователей:

```
GET /api/v1/users/
```

Добавление нового пользователя:

```
POST /api/v1/users/
```

Получение пользователя по username:

```
GET /api/v1/users/{username}/
```
#### Ресурс auth:
Запрос на получение списка произведений:

```
GET /api/v1/titles/
```

#### Ресурс titles:
Добавление произведения:

```
POST /api/v1/titles/
```

Получение информации о произведении:

```
GET /api/v1/titles/{titles_id}/
```

#### Ресурс reviews:
Получение списка всех отзывов:

```
GET /api/v1/titles/{titles_id}/reviews/
```

Добавление нового отзыва:

```
POST /api/v1/titles/{titles_id}/reviews/
```

Получение отзыва по id:

```
GET /api/v1/titles/{titles_id}/reviews/{review_id}/
```  

#### Ресурс comments:
Получение списка всех комментариев к отзыву:

```
GET /api/v1/titles/{titles_id}/reviews/{review_id}/comments/
```

Добавление комментария к отзыву:

```
POST /api/v1/titles/{titles_id}/reviews/{review_id}/comments/
```

#### Ресурсы categories и genres:
Получение списка всех категорий:

```
GET /api/v1/categories/
```

Получение списка всех жанров:

```
GET /api/v1/genres/
```

### Использованные технологии:
Python 3.9  
Django 3.2  
DRF  
JWT + Djoser  


### Авторы проекта:
[Яблокова Ирина](https://github.com/YablokovaIrina)  
[Холмаков Захар](https://github.com/kivrosa)  
[Самиляк Александр](https://github.com/aisamilyak)  
