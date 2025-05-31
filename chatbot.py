import openai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



class StreamingChatBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key="sk-vVue6LZO-ekdj84olUFL6w", base_url="https://proxy.merkulov.ai")  # Initialize OpenAI client
        self.conversation_history = []

    def add_to_history(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def print_typing_effect(self, text, delay=0.03):
        """Display text with a typing effect."""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

    def stream_response(self, user_message):
        """Get streaming response from AI."""
        self.add_to_history("user", user_message)
        print("\n🤖 ИИ думает и отвечает...")
        print("=" * 60)

        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                stream=True,
                max_tokens=500,
                temperature=0.7
            )

            full_response = ""
            word_count = 0

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    piece = chunk.choices[0].delta.content
                    print(piece, end="", flush=True)
                    full_response += piece
                    if piece == " ":
                        word_count += 1

            self.add_to_history("assistant", full_response)
            print("\n" + "=" * 60)
            print(f"📊 Статистика: {len(full_response)} символов, ~{word_count} слов")
            return full_response

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

    def show_history(self):
        """Display conversation history."""
        if not self.conversation_history:
            print("📝 История разговора пуста")
            return

        print("\n📚 История разговора:")
        print("=" * 50)
        for i, message in enumerate(self.conversation_history, 1):
            role_emoji = "👦" if message["role"] == "user" else "🤖"
            role_name = "Ты" if message["role"] == "user" else "ИИ"
            print(f"{i}. {role_emoji} {role_name}: {message['content'][:100]}...")
        print()

    def start_chat(self):
        """Start interactive chat session."""
        self.print_typing_effect("🚀 Добро пожаловать в Стриминговый Чат-Бот!", 0.05)
        print("\n💡 Советы:")
        print(" - Пиши 'выход' чтобы закончить")
        print(" - Пиши 'история' чтобы посмотреть разговор")
        print(" - Пиши 'очистить' чтобы начать заново")

        while True:
            print("\n" + "-" * 40)
            user_input = input("👦 Ты: ").strip()

            if user_input.lower() in ['выход', 'exit', 'quit']:
                self.print_typing_effect("👋 До свидания! Удачи в программировании!")
                break
            elif user_input.lower() in ['история', 'history']:
                self.show_history()
                continue
            elif user_input.lower() in ['очистить', 'clear']:
                self.conversation_history = []
                print("🧹 История разговора очищена!")
                continue
            elif not user_input:
                print("🤷 Пожалуйста, напиши что-нибудь!")
                continue

            self.stream_response(user_input)

def main():
    bot = StreamingChatBot()
    bot.start_chat()

if __name__ == "__main__":
    main()