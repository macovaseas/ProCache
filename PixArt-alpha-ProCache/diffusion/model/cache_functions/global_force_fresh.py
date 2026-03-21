from .force_scheduler import force_scheduler

s_1_injected = [1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0]

def global_force_fresh(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] == 0)
    step_index = 19 - current['step']
    is_cache_step = s_1_injected[step_index]
    threshold = 21
    
    if first_step:
        return 'full'
    else:
        if is_cache_step == 1:
            return 'full'
        elif is_cache_step == 0:
            return 'FORA'
        elif is_cache_step == 2:
            if current['layer'] < threshold:
                return 'FORA'
            else:
                return 'ToCa'