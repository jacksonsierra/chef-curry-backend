# Constraints for reaching God Mode
god_mode_point_threshold = 18
god_mode_minute_threshold = 18


# Constraints for Hot Mode
hot_mode_three_pointer_threshold = 2
hot_mode_minute_threshold = 5


# Constraints for Shot Mode
shot_mode_three_pointer_threshold = 1
shot_mode_minute_threshold = 1


# Yahoo!Sports webpage attributes
id_main = '#Main'
id_pregame = 'ul.pregame'
id_live = 'ul.in-progress'
id_final = 'ul.final'
id_steph_curry_label = '#table-1-nba\\.p\\.4612'
id_game_clock = 'ul.in-progress em.detail'
id_final_clock = 'ul.final li.status'
id_minutes_played = 'td.minutes-played'
id_field_goals = 'td.field-goals'
id_three_pointers = 'td.three-pointers'
id_free_throws = 'td.free-throws'
id_plus_minus = 'td.plus-minus'
id_off_rebounds = 'td.offensive-rebounds'
id_def_rebounds = 'td.defensive-rebounds'
id_tot_rebounds = 'td.total-rebounds'
id_assists = 'td.assists'
id_turnovers = 'td.turnovers'
id_steals = 'td.steals'
id_blocks = 'td.blocked-shots'
id_blocks_against = 'td.blocks-against'
id_personal_fouls = 'td.personal-fouls'
id_points = 'td.points-scored'

quarters = {
    '1st': 12,
    '2nd': 24,
    '3rd': 36,
    '4th': 48,
    'OT': 53,
    '2OT': 58,
    '3OT': 63,
    '4OT': 68,
    '5OT': 73
}


# Push notification messages
APNs_messages = {
    "god": "Steph Curry's in God Mode! He's already hit 18pts in the 1st Half. What are you doing looking at your phone?",
    "hot": "Chef Curry's cooking up a storm! He's drained two 3s in the last five minutes. Better go turn on the telly.",
    "shot": "It's just Steph being Steph! Just drained yet another 3. All in a day's work, literally!",
    "none": ""
}
