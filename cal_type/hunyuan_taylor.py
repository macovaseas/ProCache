from .force_scheduler import force_scheduler


s = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]

def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] < cache_dic['first_enhance'])
    force_fresh = cache_dic['force_fresh']
    step_index = current['step']
    is_cache_step = s[step_index]

    if first_step:
        current['type'] = 'full'
        current['activated_steps'].append(current['step'])
    else:
        if is_cache_step:
            current['type'] = 'full'
            current['activated_steps'].append(current['step'])
        else:
            current['type'] = 'taylor_cache'