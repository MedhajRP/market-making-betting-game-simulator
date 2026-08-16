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

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    return float(base_spread + uncertainty)

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    half_spread = spread_width / 2.0

    # Positive inventory -> shift quotes downward.
    # Negative inventory -> shift quotes upward.
    shift = inventory * skew_strength

    return {
        'bid': float(fair_value - half_spread - shift),
        'ask': float(fair_value + half_spread - shift)
    }

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    if side == 'buy':
        # Counterparty bought at our ask -> true value is likely higher.
        return float(fair_value + adjustment)

    elif side == 'sell':
        # Counterparty sold at our bid -> true value is likely lower.
        return float(fair_value - adjustment)

    return float(fair_value)

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    # Make a new dictionary so the input is not modified.
    updated_counts = dict(remaining_counts)

    # Remove one copy of the revealed card.
    if revealed_value in updated_counts:
        updated_counts[revealed_value] -= 1

        if updated_counts[revealed_value] == 0:
            del updated_counts[revealed_value]

    # Calculate the total number of remaining cards.
    total_cards = sum(updated_counts.values())

    if total_cards == 0:
        return {
            'remaining_counts': updated_counts,
            'expected_value': 0.0
        }

    # Construct the outcomes and their probabilities.
    values = list(updated_counts.keys())
    probabilities = [
        updated_counts[value] / total_cards
        for value in values
    ]

    # Reuse expected_value from the previous problem.
    mean_value = expected_value(values, probabilities)

    return {
        'remaining_counts': updated_counts,
        'expected_value': float(mean_value)
    }

# Step 13 - run_market_making_episode
def run_market_making_episode(
    true_value,
    counterparty_sides,
    initial_fair_value,
    config
):
    fair_value = float(initial_fair_value)
    cash = 0.0
    inventory = 0

    base_spread = config.get('base_spread', 0)
    uncertainty = config.get('uncertainty', 0)
    skew_strength = config.get('skew_strength', 0)
    belief_adjustment = config.get('belief_adjustment', 0)

    history = []

    # Determine the spread used throughout the episode.
    spread_width = uncertainty_spread(base_spread, uncertainty)

    for side in counterparty_sides:
        # Quote around the current fair value while accounting
        # for current inventory.
        quotes = inventory_skewed_quotes(
            fair_value,
            spread_width,
            inventory,
            skew_strength
        )

        bid = quotes['bid']
        ask = quotes['ask']

        # Execute the counterparty trade.
        state = execute_trade(
            {'cash': cash, 'inventory': inventory},
            side,
            bid,
            ask
        )

        cash = state['cash']
        inventory = state['inventory']

        # Update our fair-value belief after observing the trade.
        fair_value = update_fair_value_from_trade(
            fair_value,
            side,
            bid,
            ask,
            belief_adjustment
        )

        history.append({
            'bid': float(bid),
            'ask': float(ask),
            'side': side,
            'cash': float(cash),
            'inventory': int(inventory),
            'fair_value': float(fair_value)
        })

    # Mark remaining inventory to the true settlement value.
    pnl = mark_to_market_pnl(
        cash,
        inventory,
        true_value
    )

    return {
        'pnl': float(pnl),
        'cash': float(cash),
        'inventory': int(inventory),
        'fair_value': float(fair_value),
        'history': history
    }

# Step 14 - summarize_episode_pnls
import numpy as np

def summarize_episode_pnls(pnls):
    pnls = np.asarray(pnls, dtype=float)

    return {
        'mean': float(np.mean(pnls)),
        'std': float(np.std(pnls, ddof=0)),
        'worst': float(np.min(pnls))
    }

