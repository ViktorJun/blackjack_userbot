from pyrogram import filters, Client
from pyrogram.errors import MessageEmpty
from time import sleep
import random

api_id = your_api_id
api_hash = "your_api_hash"

app = Client("my_acc", api_id, api_hash)

# blackjack
@app.on_message(filters.command("start blackjack", prefixes=""))
def start_bd(_, msg):
    global balance
    name = msg.from_user.first_name
    balance = 1000
    msg.reply_text(f'Balance {name}: {balance}')
    # bet
    @app.on_message(filters.command("bet", prefixes="") & filters.chat(msg.chat.id))
    def bet(_, msg):
        global balance, cards_p_res, cards_d_res, bet
        msg.text = msg.text.lower()
        bet = msg.text.split('bet ', maxsplit=1)[1]
        bet = int(bet)
        if bet > balance:
            msg.reply_text('Not enough money')
        elif bet <= 0:
            msg.reply_text('You entered the wrong bid')
        else:
            # Diller
            cards_d1 = random.randint(2, 11)
            cards_d2 = random.randint(2, 10)
            cards_d_res = cards_d1 + cards_d2
            # Player
            cards_p1 = random.randint(2, 11)
            cards_p2 = random.randint(2, 10)
            cards_p_res = cards_p1 + cards_p2
            msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')

        # more
        @app.on_message(filters.command("more", prefixes="") & filters.chat(msg.chat.id))
        def more(_, msg):
            global cards_p_res, cards_d_res, balance, bet
            more = random.randint(2, 11)
            if cards_p_res > 16 and more == 11:
                cards_p_res += 1
                msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
            else:
                cards_p_res += more
                msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
            if cards_p_res > 21:
                balance -= bet
                msg.reply_text(f'Bust, the player lost\nYour balance: {balance}')

        # enough
        @app.on_message(filters.command("enough", prefixes=""))
        def enough(_, msg):
            global cards_d_res, balance, cards_p_res, bet
            while cards_d_res < 17:
                cards_d_res += random.randint(2, 10)
                msg.reply_text(f'Dealer cards: {cards_d_res}')
            if cards_d_res > 21:
                msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
                balance += bet
                msg.reply_text(f'Bust, dealer lost\nYour balance: {balance}')
            else:
                if 21 - cards_d_res > 21 - cards_p_res:
                    msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
                    balance += bet
                    msg.reply_text(f"Dealer lost\nYour balance: {balance}")
                elif 21 - cards_d_res < 21 - cards_p_res:
                    msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
                    balance -= bet
                    msg.reply_text(f"Dealer won\nYour balance: {balance}")
                else:
                    msg.reply_text(f'Dealer cards: {cards_d_res}\nCards {name}: {cards_p_res}')
                    msg.reply_text(f'Draw!\nYour balance: {balance}')
            if balance == 0:
                msg.reply_text(f'You lose\nYour balance: {balance}')


app.run()