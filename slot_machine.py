import random
import os
import keyboard
import time
import sys
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
import winsound

console = Console()

# function to get random result
def get_result():
    if random.choice(range(1, 20)) == 1:
        return "7"
    if random.choice(range(1, 15)) == 1:
        return "💎"
    if random.choice(range(1, 8)) == 1:
        return "🍋"
    if random.choice(range(1, 3)) == 1:
        return "🍒"
    else:
        return " "
    

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


# custom sounds
def spin_sound():
    # short beep to simulate spinning
    winsound.Beep(800, 50)

def win_sound():
    # three rising beeps
    for freq in [800, 1000, 1200]:
        winsound.Beep(freq, 150)

def lose_sound():
    # one low beep
    winsound.Beep(400, 200)

def game_over_sound():
    # descending beeps
    for freq in [300, 200, 100, 50, 37]:
        winsound.Beep(freq, 200)

def jackpot_sound():
    # short beeps
    staccato_freqs = [600, 650, 700, 750, 800, 850]
    for freq in staccato_freqs:
        winsound.Beep(freq, 150) 
        time.sleep(0.05) 

    # long final beep
    winsound.Beep(900, 500)


money = 100

os.system("cls" if os.name == "nt" else "clear")
console.print(Panel("🎰 Welcome to the Slot Machine! 🎰", title="Slot Machine", style="bold green"))
print("Press Enter to play or 'q' to quit: ")

key = keyboard.read_key()
if key == "q":
    print("Exiting the game. Goodbye!")
    exit()
elif key == "enter":
    pass

while True:
    clear_console()

    # simulate spinning and prevent user from holding down enter

    #hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    spinner = ["| ", "/ ", "--", "\\"]
    dots = ["", ".", "..", "..."]

    # cute little animation
    with Live(console=console, refresh_per_second=10) as live:
        duration = random.choice(range(4, 12))  # random spin duration
        for i in range(duration):  # total frames
            spin_sound()
            # wheel updates every frame
            wheel = spinner[i % len(spinner)]
            
            # dots update every 4 frames to run slower than the wheel
            dot = dots[(i // 2) % len(dots)]
            
            live.update(Text(f"Spinning{dot:<3} {wheel}", style="bold cyan"))
            time.sleep(0.08)  # frame speed


    clear_console()

    # show cursor
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

    # generate results
    result = []
    for i in range(3):
        result.append(get_result())

    # make it more likely to win
    if random.choice(range(1, 5)) == 1:
        result[1] = result[0]
        if random.choice(range(1, 3)) == 1:
            result[2] = result[0]

    # print results
    table = Table(show_header=False, show_lines=True)
    for i in range(3):
        table.add_column(justify="center")

    table.add_row(*result)

    console.print(table)

    # determine payout
    if result[0] == " ":
        payout = 0
        money -= 5
        console.print("No win, try again!", style="bold red")
        lose_sound()

    else:
        if result[0] == "🍒":
            payout = 5

        elif result[0] == "🍋":
            payout = 50

        elif result[0] == "💎":
            payout = 100

        elif result[0] == "7":
            payout = 500

        if result[0] == result[1] == result[2]:
            if result[0] == "7":
                jackpot_sound()
                console.print(f"HUGE JACKPOT!!!", style="bold yellow")
                console.print(f"You win {payout} coins!", style="bold green")
                money += payout

            else:
                win_sound()
                console.print(f"Jackpot!", style="bold yellow")
                console.print(f"You win {payout} coins!", style="bold green")
                money += payout
        else:
            console.print("No win, try again!", style="bold red")
            money -= 5
            lose_sound()
        
    # print current money
    print(f"You have {money} coins left.\n")

    # check if player is out of money
    if money <= 0:
        lose_sound()
        game_over_sound()
        console.print("You're out of money!", style="bold red")
        console.print("Do you want to reset your money to 100? (y/n): ", style="bold yellow")
        while True:
            if keyboard.is_pressed("y"):
                money = 100
                break
            elif keyboard.is_pressed("n"):
                print("Exiting the game. Goodbye!")
                exit()

    # ask to continue
    console.print("Press Enter to play again or 'q' to quit: ", style="bold yellow")
    while True:
        key = keyboard.read_key()
        if key == "q":
            console.print("Exiting the game. Goodbye!", style="bold green")
            exit()
        elif key == "enter":
            break