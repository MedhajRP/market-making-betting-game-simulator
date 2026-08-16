"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    total = 0.0
    for value, probability in zip(values, probabilities):
        total += value * probability
    return float(total)

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    # Expected value of the second roll
    faces = list(range(1, sides + 1))
    probabilities = [1.0 / sides] * sides
    reroll_value = expected_value(faces, probabilities)

    # Reroll when the first roll is strictly worse than the
    # expected value of getting a fresh roll.
    reroll_faces = [face for face in faces if face < reroll_value]

    # For each first-roll outcome, we take max(face, reroll_value).
    optimal_payoffs = [max(face, reroll_value) for face in faces]
    value = expected_value(optimal_payoffs, probabilities)

    return {
        'value': float(value),
        'reroll_faces': sorted(reroll_faces)
    }

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    faces = list(range(1, sides + 1))

    best_threshold = None
    best_value = float('-inf')

    # Suppose the threshold is t:
    #   keep t, t+1, ..., sides
    #   reroll 1, ..., t-1
    #
    # Let V be the value before a roll. If we reroll, our
    # continuation value is V - reroll_cost.
    #
    # Therefore:
    #
    # V = [sum(t..sides) + (t-1)(V - cost)] / sides
    # Solving for V gives the value associated with threshold t.
    for threshold in range(1, sides + 1):
        num_reroll_faces = threshold - 1

        sum_kept = sum(faces[threshold - 1:])

        denominator = sides - num_reroll_faces
        value = (
            sum_kept - num_reroll_faces * reroll_cost
        ) / denominator

        # A threshold t is optimal when:
        #   faces < t  should be rerolled
        #   faces >= t should be kept
        #
        # Thus the continuation value V-cost must lie between
        # t-1 and t (with equality favoring keeping the face).
        continuation_value = value - reroll_cost

        valid = (
            continuation_value <= threshold + 1e-12
            and continuation_value >= threshold - 1 - 1e-12
        )

        if valid:
            if (
                value > best_value + 1e-12
                or (
                    abs(value - best_value) <= 1e-12
                    and (best_threshold is None or threshold < best_threshold)
                )
            ):
                best_value = value
                best_threshold = threshold

    return {
        'threshold': int(best_threshold),
        'value': float(best_value)
    }

# Step 4 - red_black_card_game_value
def red_black_card_game_value(num_red, num_black):
    # Base case: no cards left
    if num_red == 0 and num_black == 0:
        return {'value': 0.0, 'stop_now': True}

    # Expected value if we continue drawing.
    total_cards = num_red + num_black

    continuation_value = 0.0

    if num_red > 0:
        red_value = red_black_card_game_value(num_red - 1, num_black)['value']
        continuation_value += (num_red / total_cards) * (1 + red_value)

    if num_black > 0:
        black_value = red_black_card_game_value(num_red, num_black - 1)['value']
        continuation_value += (num_black / total_cards) * (-1 + black_value)

    # We can always stop and receive 0.
    # Ties are resolved by stopping.
    if continuation_value <= 0:
        return {
            'value': 0.0,
            'stop_now': True
        }

    return {
        'value': float(continuation_value),
        'stop_now': False
    }

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    half_spread = spread_width / 2.0

    return {
        'bid': float(fair_value - half_spread),
        'ask': float(fair_value + half_spread)
    }

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    # Create a new state so the original is not modified.
    new_state = {
        'cash': state['cash'],
        'inventory': state['inventory']
    }

    if side == 'buy':
        # Counterparty buys from us at the ask.
        # We sell inventory and receive cash.
        new_state['cash'] += ask * size
        new_state['inventory'] -= size

    elif side == 'sell':
        # Counterparty sells to us at the bid.
        # We buy inventory and pay cash.
        new_state['cash'] -= bid * size
        new_state['inventory'] += size

    return new_state

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    # Remaining inventory is valued at the settlement value.
    return float(cash + inventory * settlement_value)

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    informed_values = np.asarray(informed_values, dtype=float)
    informed_probabilities = np.asarray(informed_probabilities, dtype=float)

    # Loss when informed trader buys from us at the ask.
    buy_loss = np.maximum(informed_values - ask, 0.0)

    # Loss when informed trader sells to us at the bid.
    sell_loss = np.maximum(bid - informed_values, 0.0)

    expected_buy_loss = np.sum(
        buy_loss * informed_probabilities
    )

    expected_sell_loss = np.sum(
        sell_loss * informed_probabilities
    )

    return float(expected_buy_loss + expected_sell_loss)

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

