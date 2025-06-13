import random

# Symbols (SCATTER/BURGER is only allowed on reels 1, 3, 5)
SYMBOLS = [
    "10", "J", "Q", "K", "A",
    "PIZZA", "FRY", "SHAKE",
    "TERRY"    # Wild
]
SCATTER = "BURGER"

REELS = 5
ROWS = 3

PAYLINES = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
]

PAYOUTS = {
    "TERRY": {3: 20, 4: 50, 5: 100},
    "SHAKE": {3: 10, 4: 20, 5: 40},
    "FRY":   {3: 8, 4: 16, 5: 32},
    "PIZZA": {3: 6, 4: 12, 5: 24},
    "A":     {3: 4, 4: 8,  5: 16},
    "K":     {3: 3, 4: 6,  5: 12},
    "Q":     {3: 2, 4: 4,  5: 8},
    "J":     {3: 1, 4: 2,  5: 4},
    "10":    {3: 0.5, 4: 1, 5: 2},
}

session_state = {
    "spin_count": 0,
    "consecutive_losses": 0,
    "terry_kick_used": False
}

def spin():
    grid = []
    for col in range(REELS):
        col_syms = []
        for row in range(ROWS):
            if col in [0, 2, 4]:  # Only allow scatter on reels 1, 3, 5 (0-indexed)
                # 1 in 8 chance for a BURGER, adjust as desired
                sym = random.choices([SCATTER] + SYMBOLS, weights=[1, 7, 7, 7, 7, 7, 7, 7, 7, 7])[0]
            else:
                # Never scatter on these reels
                sym = random.choice(SYMBOLS)
            col_syms.append(sym)
        grid.append(col_syms)
    return grid

def terry_kick_spin():
    return [
        ["FRY", "FRY", "FRY"],
        ["FRY", "FRY", "FRY"],
        ["FRY", "FRY", "FRY"],
        ["10", "J", "K"],
        ["Q", "A", "10"],
    ]

def evaluate_spin(grid):
    total_win = 0
    free_games_triggered = False

    for payline in PAYLINES:
        line_symbols = [
            grid[reel_idx][row_idx]
            for reel_idx, row_idx in enumerate(payline)
        ]

        result_symbol = None
        match_count = 0

        for symbol in line_symbols:
            if symbol == "TERRY":
                match_count += 1
                continue

            if result_symbol is None:
                result_symbol = symbol
                match_count += 1
            elif symbol == result_symbol or symbol == "TERRY":
                match_count += 1
            else:
                break

        if result_symbol and match_count >= 3:
            payout = PAYOUTS.get(result_symbol, {}).get(match_count, 0)
            total_win += payout

    # Check for BURGER on reels 1, 3, 5 (scatter)
    if (
        "BURGER" in grid[0] and
        "BURGER" in grid[2] and
        "BURGER" in grid[4]
    ):
        free_games_triggered = True

    return total_win, free_games_triggered

def generate_spin_data():
    session_state["spin_count"] += 1
    terry_kick = False

    if (
        session_state["spin_count"] <= 20 and
        session_state["consecutive_losses"] >= 5 and
        not session_state["terry_kick_used"] and
        random.random() < 0.1
    ):
        grid = terry_kick_spin()
        session_state["terry_kick_used"] = True
        terry_kick = True
    else:
        grid = spin()

    win_amount, bonus = evaluate_spin(grid)

    if win_amount > 0:
        session_state["consecutive_losses"] = 0
    else:
        session_state["consecutive_losses"] += 1

    return {
        "grid": grid,
        "win_amount": win_amount,
        "free_games_triggered": bonus,
        "terry_kick": terry_kick,
        "spin_count": session_state["spin_count"],
        "consecutive_losses": session_state["consecutive_losses"],
        "terry_kick_used": session_state["terry_kick_used"]
    }

# Debug CLI loop
if __name__ == "__main__":
    while True:
        input("\nPress Enter to spin...")
        result = generate_spin_data()

        print("\nSPIN RESULT:")
        for row in range(3):
            print(" | ".join(result["grid"][col][row] for col in range(5)))

        print(f"\nWin: ${result['win_amount']:.2f}")
        if result["free_games_triggered"]:
            print("🎉 FREE GAMES TRIGGERED!")
        if result["terry_kick"]:
            print("💢 TERRY KICKED THE MACHINE! 💢")
