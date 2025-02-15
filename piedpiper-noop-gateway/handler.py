from .util import request_new_task_id, call_noop_function, update_task_id_status
from .config import Config

def handle(request):
    """handle a request to the function
    Args:
        req (str): request body
    """
    gman_url = Config['gman']['url']

    run_id = request.get_json().get('run_id')
    project = request.get_json().get('project')
    artifacts = request.get_json().get('artifacts')
    configs = request.get_json().get('configs')
    stage = request.get_json().get('stage')

    internal_task_id = request_new_task_id(
        run_id=run_id,
        gman_url=gman_url,
        status='started',
        project=project)

    return_value = call_noop_function(run_id=run_id,
                                        faas_url="http://172.17.0.1:8080/async-function/piedpiper-noop-function",
                                        project=project,
                                        task_id=internal_task_id,
                                        stage=stage,
                                        configs=configs)

    return_value.raise_for_status()
    if return_value.status_code == 202:
        update_task_id_status(gman_url=gman_url, task_id=internal_task_id,
                              status='delegated', message='Delegated execution to noop executor', caller='noop_gateway')
        return {'task_id': internal_task_id}

    else:
        return {'task_id': return_value.status_code}

