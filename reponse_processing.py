from task_exception import TaskError
import tables
from tasks import InitTask, AcquisitionTask, ImmediateStoreTask, DelayStoreTask
import utils
from utils import Utils
import config


def handle_team_reponse(resp_data):
    teams = resp_data.get('teams')
    if teams is None:
        raise TaskError('没有获得参加本次比赛的队伍数据')
    league_id = config.league_id

    def make_team(item):
        team = dict()
        team['league_id'] = league_id
        team['team_id'] = item['team_id']
        team['team_tag'] = itme['team_tag']
        team['team_name'] = item['team_name']
        return tables.Team(team)
    team_list = map(make_team, teams)
    init = ImmediateStoreTask(team_list, Utils.get_session_make())
    init.run()
    return [InitTask(config.match_url, handle_match_reponse)]


def handle_match_reponse(resp_data):
    result = resp_data.get('result')
    if result is None:
        raise TaskError('获得的全部比赛数据有误')
    all_matches = result.get('matches')
    if all_matches is None:
        raise TaskError('获得的全部比赛数据有误')
    matches = filter(lambda x: x['start_time'] >= 1470240000, all_matches)
    matches_urls = map(
        lambda x: config.detail_url.format(x['match_id']), matches)
    return [AcquisitionTask(matches_urls, handle_detail_reponse)]


def handle_detail_reponse(resp_data):
    result = resp_data.get('result')
    if result is None:
        raise TaskError('获得的详细比赛数据有误')
    table_list = list()
    match = dict()
    match['match_id'] = result['match_id']
    match['league_id'] = result['leagueid']
    match['start_time'] = result['start_time']
    match['duration'] = result['duration']
    match['radiant_win'] = result['radiant_win']
    match['radiant_team_id'] = result['radiant_team_id']
    match['dire_team_id'] = result['dire_team_id']
    match['radiant_score'] = result['radiant_score']
    match['dire_score'] = result['dire_score']
    match['cluster'] = result['cluster']
    match_table = tables.Match(match)
    table_list.append(match_table)
    for player in result['players']:
        detail = dict()
        detail['match_id'] = result['match_id']
        detail['account_id'] = player['account_id']
        detail['player_slot'] = player['player_slot']
        detail['hero_id'] = player['hero_id']
        detail['kills'] = player['kills']
        detail['deaths'] = player['deaths']
        detail['assists'] = player['assists']
        detail['last_hits'] = player['last_hits']
        detail['denies'] = player['denies']
        detail['gold_per_min'] = player['gold_per_min']
        detail['xp_per_min'] = player['xp_per_min']
        detail['level'] = player['level']
        detail['hero_damage'] = player['hero_damage']
        detail['tower_damage'] = player['tower_damage']
        detail['hero_healing'] = player['hero_healing']
        detail['gold'] = player['gold']
        detail['gold_spent'] = player['gold_spent']
        detail_table = tables.MatchDetail(detail)
        table_list.append(detail_table)
        player_urls = list()
        if str(player['account_id']) not in utils.players:
            player_dict = dict()
            player_dict['league_id'] = config.league_id
            player_dict['account_id'] = player['account_id']
            if player['player_slot'] < 5:
                player_dict['team_id'] = result['radiant_team_id']
            else:
                player_dict['team_id'] = result['dire_team_id']
            utils.players[str(player['account_id'])] = player_dict
            player_urls.append(config.player_name_url.format(
                str(player['account_id'])))
    return [AcquisitionTask(player_urls, handle_player_response),
            DelayStoreTask(config.DELAY, table_list, Utils.get_session_make())]


def handle_player_response(resp_data):
    result = resp_data.get('profile')
    if result is None:
        raise TaskError('获得的选手数据有误')
    account_id = result['account_id']
    name = result['name']
    player = utils.players[str(account_id)]
    player['player_name'] = name
    return [DelayStoreTask(config.DELAY, [tables.Player(player)],
                           Utils.get_session_make())]
