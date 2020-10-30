import math

def d_for_equation_21(target_weight, error_margin, p, last_prefix_min=2, last_prefix_max=1000000):
    prefix_size = int((last_prefix_min + last_prefix_max) / 2)
    print(prefix_size)

    if prefix_size == last_prefix_min:
        return prefix_size

    a_weight = 1 - \
               math.pow(p, prefix_size - 1) + \
               (1 - p) / p * prefix_size * \
               (math.log(1 / (1 - p)) -
                sum([math.pow(p, i) / i for i in range(1, prefix_size)]))

    deviation = a_weight - target_weight
    if abs(a_weight - target_weight) <= error_margin:
        return p
    elif deviation < 0:  # more weight than expected --> need a greater d
        return d_for_equation_21(target_weight=target_weight,
                                 error_margin=error_margin,
                                 last_prefix_min=prefix_size,
                                 p=p,
                                 last_prefix_max=last_prefix_max)
    else:  # less weight than expected --> need a smaller d
        return d_for_equation_21(target_weight=target_weight,
                                 error_margin=error_margin,
                                 last_prefix_max=prefix_size,
                                 last_prefix_min=last_prefix_min,
                                 p=p)


def p_for_equation_21(target_weight, error_margin, prefix_size, last_p_min=0.0, last_p_max=1.0):
    p = (last_p_min + last_p_max)/2

    a_weight = 1 - \
               math.pow(p, prefix_size - 1) + \
               (1 - p) / p * prefix_size * \
               ( math.log(1 / (1-p)) -
                 sum([ math.pow(p, i)/i for i in range(1, prefix_size)]) )

    deviation = a_weight - target_weight
    if abs(a_weight - target_weight) <= error_margin:
        return p
    elif deviation > 0: # more weight than expected --> need a greater P
        return p_for_equation_21(target_weight=target_weight,
                                 error_margin=error_margin,
                                 prefix_size=prefix_size,
                                 last_p_min=p,
                                 last_p_max=last_p_max)
    else: # less weight than expected --> need a smaller P
        return p_for_equation_21(target_weight=target_weight,
                                 error_margin=error_margin,
                                 prefix_size=prefix_size,
                                 last_p_min=last_p_min,
                                 last_p_max=p)