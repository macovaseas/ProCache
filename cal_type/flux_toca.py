from .force_scheduler import force_scheduler

s = [1, 0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 2, 0, 2, 1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 1, 0, 2, 0]


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] < cache_dic['first_enhance'])
    force_fresh = cache_dic['force_fresh']
    step_index = current['step']
    is_cache_step = s[step_index]
    threshold = 30

    if first_step:
        current['type'] = 'full'
        current['activated_steps'].append(current['step'])
    else:
        if is_cache_step == 1:
            current['type'] = 'full'
            current['activated_steps'].append(current['step'])
        elif is_cache_step == 0:
            current['type'] = 'taylor_cache'
        elif is_cache_step == 'a':
            current['type'] = 'ToCa'
        else:
            current['type'] = 'taylor_cache'