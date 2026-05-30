"""
Конфигурация pytest для Django проекта BrainShare
"""

import pytest
import os
import sys
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainshare.settings')


def pytest_configure():
    """Настройка Django для pytest"""
    import django
    django.setup()