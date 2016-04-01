from pyquery import PyQuery as pq
from requests import request

import api.constants as constants


def parse_html(url):
    html = request(method='get', url=url)
    jQuery = pq(html.text)
    main = jQuery(constants.id_main)

    has_started = not main.find(constants.id_pregame)
    has_finished = bool(main.find(constants.id_final))

    if not has_started:
        return None, has_started, has_finished

    try:
        html_stats = main.find(constants.id_steph_curry_label).parent()
    except:
        return None, has_started, has_finished

    if has_finished:
        game_clock = main.find(constants.id_final_clock).text().split('-')
    else:
        game_clock = main.find(constants.id_game_clock).text().split(' ')

    corrected_game_clock = correct_game_clock(game_clock=game_clock)

    current_stats = parse_html_stats(html=html_stats)
    current_stats['minutes_elapsed'] = parse_html_time(html=corrected_game_clock)

    return current_stats, has_started, has_finished


def parse_html_stats(html):
    result = {}

    minutes_played_html = html.find(constants.id_minutes_played)
    result['minutes_played'] = parse_html_divider(value=minutes_played_html, divider=':', left=True)
    result['seconds_played'] = parse_html_divider(value=minutes_played_html, divider=':', left=False)

    field_goals_html = html.find(constants.id_field_goals)
    result['field_goals_made'] = parse_html_divider(value=field_goals_html, divider='-', left=True)
    result['field_goals_attempted'] = parse_html_divider(value=field_goals_html, divider='-', left=False)

    three_pointers_html = html.find(constants.id_three_pointers)
    result['three_pointers_made'] = parse_html_divider(value=three_pointers_html, divider='-', left=True)
    result['three_pointers_attempted'] = parse_html_divider(value=three_pointers_html, divider='-', left=False)

    free_throws_html = html.find(constants.id_free_throws)
    result['free_throws_made'] = parse_html_divider(value=free_throws_html, divider='-', left=True)
    result['free_throws_attempted'] = parse_html_divider(value=free_throws_html, divider='-', left=False)

    plus_minus_html = html.find(constants.id_plus_minus)
    result['plus_minus'] = parse_html_string(value=plus_minus_html) or '+0'

    off_rebounds_html = html.find(constants.id_off_rebounds)
    result['offensive_rebounds'] = parse_html_number(value=off_rebounds_html)

    def_rebounds_html = html.find(constants.id_def_rebounds)
    result['defensive_rebounds'] = parse_html_number(value=def_rebounds_html)

    tot_rebounds_html = html.find(constants.id_tot_rebounds)
    result['total_rebounds'] = parse_html_number(value=tot_rebounds_html)

    assists_html = html.find(constants.id_assists)
    result['assists'] = parse_html_number(value=assists_html)

    turnovers_html = html.find(constants.id_turnovers)
    result['turnovers'] = parse_html_number(value=turnovers_html)

    steals_html = html.find(constants.id_steals)
    result['steals'] = parse_html_number(value=steals_html)

    blocks_html = html.find(constants.id_blocks)
    result['blocks'] = parse_html_number(value=blocks_html)

    blocks_against_html = html.find(constants.id_blocks_against)
    result['blocks_against'] = parse_html_number(value=blocks_against_html)

    personal_fouls_html = html.find(constants.id_personal_fouls)
    result['personal_fouls'] = parse_html_number(value=personal_fouls_html)

    points_html = html.find(constants.id_points)
    result['points'] = parse_html_number(value=points_html)

    return result


def correct_game_clock(game_clock):
    time = game_clock[0].strip()
    try:
        quarter = game_clock[1].strip()
    except:
        if time == 'Final':
            return ['0:00', '4th']

        if time == 'Half':
            return ['0:00', '2nd']
    else:
        if time in ('End', 'Final'):
            return ['0:00', quarter]
        return game_clock


def parse_html_time(html):
    minutes_remaining = parse_html_divider(value=html[0], divider=':', left=True)
    quarter = parse_html_string(value=html[1])

    if quarter in constants.quarters:
        return constants.quarters[quarter] - minutes_remaining

    return 0


def parse_html_string(value):
    if not value:
        return

    try:
        result = value.text()
    except:
        result = value

    return result


def parse_html_number(value):
    if not value:
        return 0

    try:
        result = value.text()
    except:
        result = value

    try:
        result = int(result)
    except:
        return 0

    return result


def parse_html_divider(value, divider, left):
    if not value:
        return 0

    try:
        result = value.text()
    except:
        result = value

    if left:
        try:
            left_value = int(result.split(divider)[0])
        except:
            return 0

        return left_value

    try:
        right_value = int(result.split(divider)[1])
    except:
        return 0

    return right_value
