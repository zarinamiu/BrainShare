import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainshare.settings')
django.setup()

from django.contrib.auth.models import User
from communities.models import Community
from notes.models import Note
from memes.models import Meme

print("=" * 60)
print("СОЗДАНИЕ ДАННЫХ ДЛЯ BRAINSHARE")
print("=" * 60)

# Удаляем старые данные
print("\nУдаляем старые данные...")
User.objects.filter(username__in=['alex', 'maria', 'ivan', 'anna', 'dmitry', 'elena']).delete()
Community.objects.all().delete()
Note.objects.all().delete()
Meme.objects.all().delete()
print("Готово!")

# Создаём пользователей
print("\nСоздаём пользователей...")

alex = User.objects.create_user(
    username='alex',
    email='alex@brainshare.com',
    password='alex123456',
    first_name='Александр',
    last_name='Петров'
)
print(f"  + {alex.username}")

maria = User.objects.create_user(
    username='maria',
    email='maria@brainshare.com',
    password='maria123456',
    first_name='Мария',
    last_name='Иванова'
)
print(f"  + {maria.username}")

ivan = User.objects.create_user(
    username='ivan',
    email='ivan@brainshare.com',
    password='ivan123456',
    first_name='Иван',
    last_name='Сидоров'
)
print(f"  + {ivan.username}")

anna = User.objects.create_user(
    username='anna',
    email='anna@brainshare.com',
    password='anna123456',
    first_name='Анна',
    last_name='Козлова'
)
print(f"  + {anna.username}")

dmitry = User.objects.create_user(
    username='dmitry',
    email='dmitry@brainshare.com',
    password='dmitry123456',
    first_name='Дмитрий',
    last_name='Новиков'
)
print(f"  + {dmitry.username}")

elena = User.objects.create_user(
    username='elena',
    email='elena@brainshare.com',
    password='elena123456',
    first_name='Елена',
    last_name='Смирнова'
)
print(f"  + {elena.username}")

# Создаём сообщества
print("\nСоздаём сообщества...")

comm1 = Community.objects.create(
    name='Python Developers',
    description='Сообщество Python разработчиков. Обсуждаем лучшие практики, библиотеки и фреймворки.'
)
print(f"  + {comm1.name}")

comm2 = Community.objects.create(
    name='Django Fans',
    description='Для всех, кто любит Django! Делимся опытом, задаём вопросы.'
)
print(f"  + {comm2.name}")

comm3 = Community.objects.create(
    name='JavaScript Lovers',
    description='JavaScript - наш лучший друг! React, Vue, Angular и многое другое.'
)
print(f"  + {comm3.name}")

comm4 = Community.objects.create(
    name='SQL Masters',
    description='Всё о базах данных и SQL-запросах. PostgreSQL, MySQL, SQLite.'
)
print(f"  + {comm4.name}")

comm5 = Community.objects.create(
    name='Study Group',
    description='Вместе учиться веселее! Делимся конспектами и помогаем друг другу.'
)
print(f"  + {comm5.name}")

comm6 = Community.objects.create(
    name='Backend Developers',
    description='Бэкенд - это не только API. Обсуждаем архитектуру, базы данных, микросервисы.'
)
print(f"  + {comm6.name}")

# Создаём конспекты
print("\nСоздаём конспекты...")

note1_content = """# Python: Переменные и типы данных

## Что такое переменная?
Переменная - это именованная область памяти для хранения данных.

### Создание переменных:
name = "Alice"
age = 25
height = 1.75
is_student = True

## Основные типы данных:
- int - целые числа (42, -17, 0)
- float - дробные числа (3.14, -2.5)
- str - строки ("Hello")
- bool - логические (True, False)
- list - списки ([1, 2, 3])
- dict - словари ({"key": "value"})"""

note1 = Note.objects.create(
    title='Python: Переменные и типы данных',
    content=note1_content,
    author=alex,
    subject='Python',
    is_public=True
)
print(f"  + {note1.title}")

note2_content = """# Python: Условия и циклы

## Условные конструкции:
age = 18

if age < 18:
    print("Несовершеннолетний")
elif age == 18:
    print("Только исполнилось 18!")
else:
    print("Совершеннолетний")

## Цикл for:
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

## Цикл while:
count = 0
while count < 5:
    print(count)
    count += 1"""

note2 = Note.objects.create(
    title='Python: Условия и циклы',
    content=note2_content,
    author=alex,
    subject='Python',
    is_public=True
)
print(f"  + {note2.title}")

note3_content = """# SQL: Основы SELECT запросов

## Базовый синтаксис:
SELECT column1, column2 FROM table_name;

## Выборка данных:
SELECT * FROM users;
SELECT name, email FROM users;

## Фильтрация с WHERE:
SELECT * FROM users WHERE age > 18;
SELECT * FROM products WHERE price BETWEEN 100 AND 500;

## Сортировка ORDER BY:
SELECT * FROM products ORDER BY price ASC;
SELECT * FROM products ORDER BY price DESC;"""

note3 = Note.objects.create(
    title='SQL: Основы SELECT',
    content=note3_content,
    author=maria,
    subject='SQL',
    is_public=True
)
print(f"  + {note3.title}")

note4_content = """# Django: Создание моделей

## Базовый пример:
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

## Миграции:
python manage.py makemigrations
python manage.py migrate"""

note4 = Note.objects.create(
    title='Django: Создание моделей',
    content=note4_content,
    author=ivan,
    subject='Django',
    is_public=True
)
print(f"  + {note4.title}")

note5_content = """# JavaScript: Основы синтаксиса

## Переменные:
let name = "John";
const PI = 3.14159;

## Функции:
function greet(name) {
    return "Hello, " + name + "!";
}

const add = (a, b) => a + b;

## Циклы:
for (let i = 0; i < 5; i++) {
    console.log(i);
}"""

note5 = Note.objects.create(
    title='JavaScript: Основы',
    content=note5_content,
    author=anna,
    subject='JavaScript',
    is_public=True
)
print(f"  + {note5.title}")

note6_content = """# HTML/CSS: Flexbox

## Flex-контейнер:
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}

## Центрирование элемента:
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

## Основные свойства:
- flex-direction - направление оси
- justify-content - выравнивание по главной оси
- align-items - выравнивание по поперечной оси
- flex-wrap - перенос элементов
- gap - отступы между элементами"""

note6 = Note.objects.create(
    title='HTML/CSS: Flexbox',
    content=note6_content,
    author=dmitry,
    subject='HTML/CSS',
    is_public=True
)
print(f"  + {note6.title}")

note7_content = """# Git: Основные команды

## Начало работы:
git init
git clone https://github.com/user/repo.git

## Основные команды:
git status
git add .
git commit -m "Сообщение"
git push origin main
git pull origin main

## Ветки:
git branch feature-name
git checkout feature-name
git checkout -b feature
git merge feature-name"""

note7 = Note.objects.create(
    title='Git: Основные команды',
    content=note7_content,
    author=elena,
    subject='Git',
    is_public=True
)
print(f"  + {note7.title}")

# Создаём мемы
print("\nСоздаём мемы...")

meme1 = Meme.objects.create(
    title='Когда код заработал с первого раза',
    image_url='https://media.giphy.com/media/XreQmk7ETCak0/giphy.gif',
    description='Невероятное чувство, когда ничего не пришлось дебажить!',
    author=alex,
    category='Программирование'
)
print(f"  + {meme1.title}")

meme2 = Meme.objects.create(
    title='JavaScript за неделю до дедлайна',
    image_url='https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif',
    description='Когда понимаешь, что ничего не успеваешь',
    author=ivan,
    category='JavaScript'
)
print(f"  + {meme2.title}")

meme3 = Meme.objects.create(
    title='SQL в реальной жизни',
    image_url='https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif',
    description='SELECT * FROM motivation WHERE deadline = tomorrow',
    author=maria,
    category='SQL'
)
print(f"  + {meme3.title}")

meme4 = Meme.objects.create(
    title='Python vs JavaScript',
    image_url='https://media.giphy.com/media/l0MYt5jPRqQX5pnqM/giphy.gif',
    description='Вечный спор, который никогда не закончится',
    author=anna,
    category='Программирование'
)
print(f"  + {meme4.title}")

meme5 = Meme.objects.create(
    title='Django debug',
    image_url='https://media.giphy.com/media/l46Cy1mH9vXatyPKY/giphy.gif',
    description='Когда 500 ошибка, а ты не знаешь почему',
    author=dmitry,
    category='Django'
)
print(f"  + {meme5.title}")

meme6 = Meme.objects.create(
    title='Код с ChatGPT',
    image_url='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHQ5YWVtM2JwcTd0Z3JqYmZnMnNqNzdxYnIycGFiZGRnaWxsMXBoMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/du3E3CAlhom2R04UQc/giphy.gif',
    description='Скопировал, вставил, работает. Идеально!',
    author=elena,
    category='Программирование'
)
print(f"  + {meme6.title}")

meme7 = Meme.objects.create(
    title='HTML vs CSS vs JavaScript',
    image_url='https://media.giphy.com/media/LmNwrBhejkK9EFP50V/giphy.gif',
    description='Троица фронтенда',
    author=ivan,
    category='Frontend'
)
print(f"  + {meme7.title}")

meme8 = Meme.objects.create(
    title='Когда сдал курсовую',
    image_url='https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif',
    description='Наконец-то можно поспать!',
    author=anna,
    category='Учеба'
)
print(f"  + {meme8.title}")

print("\n" + "=" * 60)
print("ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
print("=" * 60)
print(f"\nИтого создано:")
print(f"   Пользователей: 6")
print(f"   Сообществ: 6")
print(f"   Конспектов: 7")
print(f"   Мемов: 8")