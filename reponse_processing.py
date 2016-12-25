from task_exception import TaskError
import tables
from tasks import InitTask, AcquisitionTask, ImmediateStoreTask, DelayStoreTask
import utils
from utils import Utils
import config
import players


def handle_team_reponse(resp_data):
    teams = resp_data.get('teams')
    if teams is None:
        raise TaskError('没有获得参加本次比赛的队伍数据')
    league_id = config.league_id

    def make_team(item):
        item['league_id'] = league_id
        team = tables.Team(item)
        return team
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
    match_table = Match(match)
    detail = dict()
