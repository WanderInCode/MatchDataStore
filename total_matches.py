from task_exception import TaskException


def handle_reponse(resp_data):
    result = resp_data.get('result')
    if result is None:
        raise TaskException('获得的全部比赛数据有误')
    all_matches = result.get('matches')
    if all_matches is None:
        raise TaskException('获得的全部比赛数据有误')
    matches = filter(lambda x: x['start_time'] >= 1470240000, all_matches)
    # TODO need to return custom Task object
    return matches
