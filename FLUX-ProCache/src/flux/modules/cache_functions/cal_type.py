from .force_scheduler import force_scheduler

# ProCache style

# s_1_injected = [1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# def cal_type(cache_dic, current):
#     '''
#     Determine calculation type for this step
#     '''
#     first_step = (current['step'] < cache_dic['first_enhance'])
#     step_index = current['step']
#     is_cache_step = s_1_injected[step_index]
#     threshold = 18
#     # current['type'] = 'full'
#     # current['activated_steps'].append(current['step'])

#     if first_step:
#         current['type'] = 'full'
#         if current['step'] not in current['activated_steps']:
#             current['activated_steps'].append(current['step'])
#     else:
#         # 设置计算类型
#         if is_cache_step == 1:
#             current['type'] = 'full'
#             if current['step'] not in current['activated_steps']:
#                 current['activated_steps'].append(current['step'])
#         elif is_cache_step == 0:
#             current['type'] = 'FORA'
#         elif is_cache_step == 2:
#             if current['layer'] < threshold:
#                 current['type'] = 'FORA'
#             else:
#                 current['type'] = 'ToCa'


# TaylorSeer style

s_1_injected = [1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 1, 0, 2, 0, 2, 1, 0, 2, 0, 2, 1, 0, 2, 0, 2]


def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    first_step = (current['step'] < cache_dic['first_enhance'])
    step_index = current['step']
    is_cache_step = s_1_injected[step_index]

    if first_step:
        current['type'] = 'full'
        if current['step'] not in current['activated_steps']:
            current['activated_steps'].append(current['step'])
    else:
        # 设置计算类型
        if is_cache_step == 1:
            current['type'] = 'full'
            if current['step'] not in current['activated_steps']:
                current['activated_steps'].append(current['step'])
        else:
            current['type'] = 'taylor_cache'