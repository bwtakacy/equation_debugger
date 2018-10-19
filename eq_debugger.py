from sympy import *

def preprocess(expr_str):
    expr_str = expr_str.replace('\u3000', '')
    expr_str = expr_str.replace(' ','')
    expr_str = expr_str.replace('ー', '-')
    expr_str = expr_str.replace('－', '-')
    expr_str = expr_str.replace('＋','+')
    expr_str = expr_str.replace('（','(')
    expr_str = expr_str.replace('）',')')
    expr_str = expr_str.replace('(','(')
    expr_str = expr_str.replace(')',')')
    expr_str = expr_str.replace('＝','=')
    expr_str = expr_str.replace('/', '/')
    return expr_str

def check_single(expr):
    if expr.is_number:
        return True
    coeffs = Poly(expr).all_coeffs()
    is_single = False
    if coeffs[0] != 0:
        if sum(coeffs[1:]) == 0:
            is_single = True
    return is_single

def check_equation_validity(str1, str2):
    x = Symbol("x")
    p_str1 = preprocess(str1)
    p_str2 = preprocess(str2)
    expr_1_l = sympify(p_str1.split(sep="=")[0])
    expr_1_r = sympify(p_str1.split(sep="=")[1])
    expr_2_l = sympify(p_str2.split(sep="=")[0])
    expr_2_r = sympify(p_str2.split(sep="=")[1])

    is_valid = False
    reason = ""

    if expr_1_l.is_number and expr_2_l.is_number:
        q_l, r_l = div(expr_1_l * x, expr_2_l * x)
    else:
        q_l, r_l = div(expr_1_l, expr_2_l)
        is_single_1 = check_single(expr_1_l)
        is_single_2 = check_single(expr_2_l)
    #print("q_l:{0}, r_l:{1}".format(q_l, r_l))
    if expr_1_r.is_number and expr_2_r.is_number:
        if expr_1_r != 0 and expr_2_r != 0:
            q_r, r_r = div(expr_1_r * x, expr_2_r * x)
        else:
            q_r, r_r = 0,0
    else:
        q_r, r_r = div(expr_1_r, expr_2_r)
        is_single_1 = check_single(expr_1_r)
        is_single_2 = check_single(expr_2_r)
    #print("q_r:{0}, r_r:{1}".format(q_r, r_r))
    q_all, r_all = div(simplify(expr_1_l - expr_1_r), simplify(expr_2_l - expr_2_r))
    print("q_all:{0}, r_all{1}".format(q_all,r_all))

    #項が一つの場合
    if is_single_1 and is_single_2:
        if expr_1_l == expr_2_l * q_l and expr_1_r == expr_2_r * q_l:
            is_valid = True
            reason = "正常：両辺定数倍"
        else:
            reason = "両辺の定数倍計算にミスがあります(error_1)"

        return (is_valid, reason)

    # 項が複数ある場合
    if q_all.is_number and r_all == 0:
        if simplify(expr_1_l - expr_1_r - q_all * (expr_2_l - expr_2_r)) == 0:
            is_valid = True
            reason = "正常：両辺定数倍しつつ移行変形"
        else:
            reason = "両辺の定数倍・移行計算にミスがあります(error_7)"
    elif q_l == q_r:
        if expr_1_l == expr_2_l * q_l and expr_1_r == expr_2_r * q_r:
            is_valid = True
            reason = "正常：両辺定数倍"
        else:
            reason = "両辺の定数倍計算にミスがあります(error_6)"
    elif expr_1_l == expr_2_l and expr_1_r == expr_2_r:
        is_valid = True
        reason = "正常：展開or項整理or式変形なし"
    elif expr_1_l == expr_2_l:
        if simplify(expr_1_r - expr_2_r) == 0:
            is_valid = True
            reason = "正常：右辺のみ変形"
        else:
            reason = "右辺の変形にミスがあります(error_2)"
    elif expr_1_r == expr_2_r:
        if simplify(expr_1_l - expr_2_l) == 0:
            is_valid = True
            reason = "正常：左辺のみ変形"
        else:
            reason = "左辺の変形にミスがあります(error_3)"
    elif simplify(expr_1_l - expr_2_l) == 0:
        if simplify(expr_1_r - expr_2_r) == 0:
            is_valid = True
            reason = "正常：両辺変形"
        else:
            reason = "右辺の変形にミスがあります(error_4)"
    elif simplify(expr_1_r - expr_2_r) == 0:
        if simplify(expr_1_l - expr_2_l) == 0:
            is_valid = True
            reason = "正常：両辺変形"
        else:
            reason = "左辺の変形にミスがあります(error_5)"
    elif simplify(expr_1_l - expr_1_r) == simplify(expr_2_l - expr_2_r):
        is_valid = True
        reason = "正常：移項変形"
    else:
        reason = "左辺と右辺の移項変形にミスがあります(error_7)"
    return (is_valid, reason)

def check_total_answer(answer_str):
    exprs = answer_str.split(sep="\n")
    result = []
    for i in range(len(exprs)):
        if i == len(exprs)-1:
            break
        try:
            step = "Checking transformation from [{0}] to [{1}]".format(exprs[i],exprs[i+1])
            print(step)
            res = check_equation_validity(exprs[i], exprs[i+1])
            print(res)
            result.append((step,res))
        except Exception as e:
            print(e)
            result.append(str(e))
    return result
