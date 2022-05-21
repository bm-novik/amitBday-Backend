import math


def calc(rating_list):
    judges_count = 0
    judges_score = 0
    audience_score = 0
    for rating in rating_list:
        if rating['user__is_staff']:
            judges_score += rating['rating']
            judges_count += 1
        else:
            audience_score += rating['rating']
    overall_score = judges_score + audience_score
    judges = math.floor((judges_count * 12 / judges_score) * (overall_score * 0.4))
    audience = math.floor(((len(rating_list) - judges_count) * 12 / audience_score) * (overall_score * 0.6))

    return {
        "overall": judges + audience,
        "judges": judges,
        "audience": audience
    }
