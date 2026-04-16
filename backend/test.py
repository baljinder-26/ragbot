from backend import ask_bot

history = []

while True:

    user_input = input("User: ")

    if user_input == "exit":
        break

    reply = ask_bot(
        user_input,
        history
    )

    print("Bot:", reply)