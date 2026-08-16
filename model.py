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

# Step 4 - red_black_card_game_value (not yet solved)
# TODO: implement

# Step 5 - make_quotes (not yet solved)
# TODO: implement

# Step 6 - execute_trade (not yet solved)
# TODO: implement

# Step 7 - mark_to_market_pnl (not yet solved)
# TODO: implement

# Step 8 - adverse_selection_loss (not yet solved)
# TODO: implement

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

