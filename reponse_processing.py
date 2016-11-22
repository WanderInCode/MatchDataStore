from task_exception import TaskException


# TODO
def handle_initial_reponse(resp_data):
    result = resp_data.get('result')
    if result is None:
        raise TaskException('获得的全部比赛数据有误')
    all_matches = result.get('matches')
    if all_matches is None:
        raise TaskException('获得的全部比赛数据有误')
    matches = filter(lambda x: x['start_time'] >= 1470240000, all_matches)
    # TODO need to return MatchTask object
    return matches


def handle_match_reponse(resp_data):
    pass


def handle_detail_reponse(resp_data):
    pass


def handle_team_reponse(resp_data):
    result = resp_data.get('teams')
    if result is None:
        raise TaskException('没有获得参加本次比赛的队伍数据')
    # TODO
    task = StoreTask()
