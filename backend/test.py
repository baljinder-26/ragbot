from backend.engine import chat

history = []

while True:

    user_input = input("User: ")

    if user_input == "exit":
        break

    reply = chat(
        user_input,
        "test_user"
    )

    print("Bot:", reply)