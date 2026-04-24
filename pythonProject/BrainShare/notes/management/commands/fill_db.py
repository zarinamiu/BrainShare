from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notes.models import Note, Comment
from communities.models import Community, CommunityMembership
from memes.models import Meme
from users.models import Profile
import random


class Command(BaseCommand):
    help = 'Автозаполнение базы данных тестовыми данными для BrainShare'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notes',
            type=int,
            default=10,
            help='Количество конспектов для создания'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Количество пользователей для создания'
        )
        parser.add_argument(
            '--communities',
            type=int,
            default=3,
            help='Количество сообществ для создания'
        )
        parser.add_argument(
            '--memes',
            type=int,
            default=5,
            help='Количество мемов для создания'
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаем заполнение базы данных BrainShare...')

        subjects = [
            'Математика', 'Физика', 'Химия', 'Биология', 'История',
            'Литература', 'Информатика', 'Английский', 'География', 'Экономика'
        ]

        note_titles = [
            'Основы теории вероятностей',
            'Законы Ньютона',
            'Органическая химия',
            'Клеточная биология',
            'Великая Отечественная война',
            'Творчество Пушкина',
            'Алгоритмы и структуры данных',
            'Английские времена',
            'География России',
            'Микроэкономика',
            'Интегралы и производные',
            'Квантовая физика',
            'Электрохимия',
            'Генетика',
            'Древний Рим',
            'Русская классика',
            'ООП в Python',
            'Бизнес-английский',
            'Климат и погода',
            'Макроэкономика'
        ]

        community_names = [
            'Математический кружок',
            'Физики-теоретики',
            'Программисты BrainShare',
            'Гуманитарии',
            'Биологическая лаборатория',
            'Исторический клуб',
            'Английский для всех'
        ]

        self.stdout.write('👤 Создание пользователей...')
        users = []

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@brainshare.ru',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            Profile.objects.get_or_create(user=admin)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Создан админ: {admin.username}'))
        else:
            self.stdout.write(f'  → Админ уже существует: {admin.username}')
        users.append(admin)

        test_users_data = [
            ('student1', 'student1@brainshare.ru'),
            ('student2', 'student2@brainshare.ru'),
            ('student3', 'student3@brainshare.ru'),
            ('teacher1', 'teacher1@brainshare.ru'),
            ('researcher1', 'researcher1@brainshare.ru'),
        ]

        for i in range(options['users']):
            if i < len(test_users_data):
                username, email = test_users_data[i]
            else:
                username = f'user{i}'
                email = f'user{i}@brainshare.ru'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            if created:
                user.set_password('test12345')
                user.save()
                Profile.objects.get_or_create(user=user)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Создан пользователь: {username}'))
            else:
                self.stdout.write(f'  → Пользователь уже существует: {username}')
            users.append(user)

        self.stdout.write('👥 Создание сообществ...')

        for i in range(options['communities']):
            if i < len(community_names):
                name = community_names[i]
            else:
                name = f'Сообщество {i + 1}'

            community, created = Community.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'Описание сообщества {name}. Здесь обсуждают интересные темы!',
                    'creator': random.choice(users),
                    'is_private': random.choice([True, False])
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Создано сообщество: {name}'))
                # Добавляем участников
                for user in random.sample(users, min(3, len(users))):
                    CommunityMembership.objects.get_or_create(
                        community=community,
                        user=user,
                        defaults={'role': random.choice(['member', 'moderator'])}
                    )
            else:
                self.stdout.write(f'  → Сообщество уже существует: {name}')

        self.stdout.write('📝 Создание конспектов...')

        # ИСПРАВЛЕНО: русский текст вместо Lorem Ipsum
        lorem_texts = [
            'Добро пожаловать в конспект! Здесь собраны основные определения и формулы, '
            'которые помогут вам в изучении данной темы. Внимательно прочитайте материал.',
            'Рассмотрим основные понятия и теоремы. Для начала разберём определения, '
            'затем перейдём к практическим примерам и задачам для самостоятельного решения.',
            'Важные формулы и уравнения, которые необходимо запомнить. '
            'Рекомендуется выучить их наизусть и применять при решении задач.',
            'Примеры решения типовых задач. Внимательно изучите ход рассуждений '
            'и попробуйте решить похожие задачи самостоятельно.',
            'Дополнительные материалы и ссылки на источники. '
            'Здесь вы найдёте литературу и ресурсы для более глубокого изучения темы.'
        ]

        for i in range(options['notes']):
            title = note_titles[i % len(note_titles)]
            subject = subjects[i % len(subjects)]
            author = random.choice(users)

            note, created = Note.objects.get_or_create(
                title=f'{title} #{i + 1}',
                defaults={
                    'content': '\n\n'.join(random.sample(lorem_texts, 3)),
                    'author': author,
                    'subject': subject,
                    'is_public': True,
                    'views_count': random.randint(0, 500)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Создан конспект: {note.title}'))

                for j in range(random.randint(0, 3)):
                    commenter = random.choice(users)
                    Comment.objects.get_or_create(
                        note=note,
                        author=commenter,
                        text=f'Отличный конспект по {subject}! Спасибо за материал.'
                    )
            else:
                self.stdout.write(f'  → Конспект уже существует: {title}')

        self.stdout.write('😂 Создание мемов...')

        meme_titles = [
            'Когда понял тему за минуту до сдачи',
            'Студент на сессии',
            'Программист ищет баг',
            'Утро перед экзаменом',
            'Когда код заработал с первого раза',
            'deadline в 23:59',
            'Открыл учебник за час до зачёта'
        ]

        for i in range(options['memes']):
            title = meme_titles[i % len(meme_titles)]
            author = random.choice(users)

            meme, created = Meme.objects.get_or_create(
                title=f'{title} #{i + 1}',
                defaults={
                    'author': author,
                    'description': f'Мем на тему: {title}',
                    'is_approved': True,
                    'likes_count': random.randint(0, 100)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Создан мем: {meme.title}'))
            else:
                self.stdout.write(f'  → Мем уже существует: {title}')

        self.stdout.write(self.style.SUCCESS('\n✅ База данных успешно заполнена!'))
        self.stdout.write(f'''
📊 Статистика:
   👤 Пользователей: {User.objects.count()}
   📝 Конспектов: {Note.objects.count()}
   💬 Комментариев: {Comment.objects.count()}
   👥 Сообществ: {Community.objects.count()}
   😂 Мемов: {Meme.objects.count()}
''')