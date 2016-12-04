from key import key

league_id = 4664

team_url = 'http://api.steampowered.com/IDOTA2Teams_570/GetTeamInfo/v1/?key={}&league_id={}'.format(
    key, league_id)

match_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?key={}&league_id={}'.format(
    key, league_id)

detail_url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key={}&match_id={}'.format(
    key, '{}')
