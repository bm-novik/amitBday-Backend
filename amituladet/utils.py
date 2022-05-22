import json
import math


def calc_results(max_rating_score, song, max_possible_result, group_classification, group_percent):
    actual_percent = song[f'{group_classification}_score'] / (max_rating_score * song[f'{group_classification}_count'])
    max_score_for_group = max_possible_result * group_percent
    return max_score_for_group * actual_percent


def clean_rating_data(list):
    agg_dict = {}

    for score_item in list:
        key = score_item['song__id']
        if not agg_dict.get(score_item['song__id']):
            agg_dict[key] = {
                "song_name": '',
                "singer": '',
                "judges_count": 0,
                "audience_count": 0,
                "judges_score": 0,
                "audience_score": 0,
            }
            agg_dict[key]['song_name'] = score_item['song__song']
            agg_dict[key]['singer'] = score_item['song__singer']

        score_item_classification = 'judges' if score_item['user__is_staff'] else 'audience'
        agg_dict[key][f'{score_item_classification}_score'] += score_item['sum']
        agg_dict[key][f'{score_item_classification}_count'] += score_item['count']

    return agg_dict


def calc_and_stringify(rating_list):
    max_rating_score = 12
    judges_percent = 0.4
    audience_percent = 0.6
    ret_list = []

    res_dict = clean_rating_data(rating_list)

    for song_id, song_details in res_dict.items():
        max_possible_result = (song_details['judges_count'] + song_details['audience_count']) * max_rating_score

        judges = calc_results(
            max_rating_score=max_rating_score,
            song=song_details,
            max_possible_result=max_possible_result,
            group_classification='judges',
            group_percent=judges_percent
        ) if song_details['judges_count'] > 0 else 0

        audience = calc_results(
            max_rating_score=max_rating_score,
            song=song_details,
            max_possible_result=max_possible_result,
            group_classification='audience',
            group_percent=audience_percent
        ) if song_details['audience_count'] > 0 else 0

        ret_list.append(
            {
                'song_id': song_id,
                "song_name": song_details["song_name"],
                "singer": song_details["singer"],
                'overall_score': math.floor(judges) + math.floor(audience),
                'actual_judges_score': judges,
                'judges_score': math.floor(judges),
                'actual_audience_score': audience,
                'audience_score': math.floor(audience)
            }
        )
    return sorted(ret_list, key=lambda x: x['actual_judges_score'] + x['actual_audience_score'], reverse=True)

