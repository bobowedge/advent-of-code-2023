def hand_type(hand):
    cards = set(hand)
    if len(cards) == 1:
        hand_type = 7
    elif len(cards) == 2:
        card = cards.pop()
        if hand.count(card) == 2 or hand.count(card) == 3:
            hand_type = 5
        else:
            hand_type = 6
    elif len(cards) == 3:
        card = cards.pop()
        while hand.count(card) == 1:
            card = cards.pop()
        if hand.count(card) == 2:
            hand_type = 3
        else:
            hand_type = 4
    elif len(cards) == 4:
        hand_type = 2
    else:
        hand_type = 1
    return hand_type


def sort_key1(hand):
    ht = hand_type(hand)
    card_int = {f'{x}': x for x in range(2, 10)}
    card_int.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})
    result = [card_int[c] for c in hand]
    result = [ht] + result
    return tuple(result)


def solution1(d):
    bids = {}
    hands = []
    for line in d:
        hand, bid = line.split()
        hands.append(hand)
        if hand in bids:
            raise RuntimeError("duplicate")
        bids[hand] = int(bid)
    hands.sort(key=sort_key1)
    total = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        bid = bids[hand]
        total += rank * bid
    return total


def sort_key2(hand):
    if 'J' in hand:
        max_ht = 1
        for wildcard in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']:
            new_hand = hand.replace('J', wildcard)
            new_ht = hand_type(new_hand)
            max_ht = max(max_ht, new_ht)
    else:
        max_ht = hand_type(hand)
    card_int = {f'{x}': x for x in range(2, 10)}
    card_int.update({'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14})
    result = [card_int[c] for c in hand]
    result = [max_ht] + result
    return tuple(result)


def solution2(d):
    bids = {}
    hands = []
    for line in d:
        hand, bid = line.split()
        hands.append(hand)
        if hand in bids:
            raise RuntimeError("duplicate")
        bids[hand] = int(bid)
    hands.sort(key=sort_key2)
    total = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        bid = bids[hand]
        total += rank * bid
    return total


test = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.splitlines()
assert(solution1(test) == 6440)
assert(solution2(test) == 5905)

data = open("data/day07.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
