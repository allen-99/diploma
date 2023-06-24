#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diploma.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def create_bag_of_words(text):
    text_split = text.split()
    bag_of_words = {}
    for token in text_split:
        bag_of_words[token] = bag_of_words.get(token, 0) + 1
    return bag_of_words


if __name__ == '__main__':
    main()
