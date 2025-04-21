from uuid import uuid4
from nicegui import ui
import re

messages = []

# List of abusive words to filter
bad_words = ['idiot', 'dumb', 'stupid', 'fuck you', 'bitch']

def filter_message(message):
    # Replace each bad word with asterisks
    for word in bad_words:
        pattern = rf'\b{word}\b'
        message = re.sub(pattern, '*' * len(word), message, flags=re.IGNORECASE)
    return message

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id == own_id)

@ui.page('/')
def index():
    def send():
        clean_text = filter_message(text.value)
        messages.append((user, avatar, clean_text))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)

ui.run()
