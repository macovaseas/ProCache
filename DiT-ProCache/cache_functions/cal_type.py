s = [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] == (current['num_steps'] - 1))    
    step_index = 49 - current['step']
    is_cache_step = s[step_index]
    threshold = 21
    
    if first_step:
        current['type'] = 'full'
    else:
        if is_cache_step == 1:
            current['type'] = 'full'
        elif is_cache_step == 0:
            current['type'] = 'FORA'
        elif is_cache_step == 2:
            if current['layer'] < threshold:
                current['type'] = 'FORA'
            else:
                current['type'] = 'ToCa'
        else:
            current['type'] = 'FORA'
