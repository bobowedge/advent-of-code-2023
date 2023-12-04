def score_card(card):
    card_num, all_numbers = card.split(':')
    card_num = int(card_num.split()[-1])
    winning_numbers, your_numbers = all_numbers.split('|')
    winning_numbers = set([int(x) for x in winning_numbers.split()])
    your_numbers = set([int(x) for x in your_numbers.split()])
    matches = len(your_numbers.intersection(winning_numbers))
    return card_num, matches


def solution1(d):
    total_score = 0
    for line in d:
        _, score = score_card(line)
        if score > 0:
            total_score += 2**(score-1)
    return total_score


def solution2(d):
    cards = {i: 1 for i in range(1, len(d)+1)}
    for line in d:
        card_num, score = score_card(line)
        for i in range(card_num+1, card_num+score+1):
            cards[i] = cards.get(i, 0) + cards[card_num]
    print(cards)
    total_cards = 0
    for num in cards.values():
        total_cards += num
    return total_cards


test = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.splitlines()
assert(solution1(test) == 13)
assert(solution2(test) == 30)


data = open('data/day04.txt').read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
