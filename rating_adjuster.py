def apply_review_balancer(movies):
    max_reviews = max(movie['num_reviews'] for movie in movies)
    
    for movie in movies:
        diff = max_reviews - movie['num_reviews']
        penalty = (diff // 100000) * 0.1
        movie['adjusted_rating'] = round(movie['rating'] - penalty, 2)

def apply_oscar_bonus(movies):
    for movie in movies:
        oscars = movie['num_oscars']
        bonus = 0.0
        if oscars >= 1 and oscars <= 2:
            bonus = 0.3
        elif oscars >= 3 and oscars <= 5:
            bonus = 0.5
        elif oscars >= 6 and oscars <= 10:
            bonus = 1.0
        elif oscars > 10:
            bonus = 1.5
        movie['adjusted_rating'] = round(movie['adjusted_rating'] + bonus, 2)
