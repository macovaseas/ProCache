s = [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]


# def cal_type(cache_dic, current):
#     '''
#     Determine calculation type for this step
#     '''
#     last_steps = (current['step'] <=2)
#     first_step = (current['step'] == (current['num_steps'] - 1))
#     force_fresh = cache_dic['force_fresh']
#     if not first_step:
#         fresh_interval = cache_dic['cal_threshold']
#     else:
#         fresh_interval = cache_dic['fresh_threshold']

#     if (current['step'] % fresh_interval == 0) or first_step:
#         current['type'] = 'full'
        
#     elif ((current['step'] % fresh_interval) % 2 == 1): #[1,3,5] [2,4,6]
#         current['type'] = 'ToCa'
#     # 'ToCa' 'FORA'
#     else: 
#         current['type'] = 'ToCa'


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] == (current['num_steps'] - 1))    
    step_index = current['step']
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