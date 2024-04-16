import numpy as np


def push_f(f_init, coeffs):
    f_result = 0
    for i in range(1, len(coeffs)):
        f_result += f_init[i-1] * -coeffs[i]
    return f_result / coeffs[0]


def update_f(f, f_vector):
    new_f = f_vector[:len(f_vector) - 1]  # .pop(len(f_vector) - 1)
    new_f = np.insert(new_f, 0, f)
    return new_f


def c_func(ct, ct1):
    return (ct1*ct+1)/(2*ct)


def sine(cosine):
    return np.sqrt(1-cosine**2)


# coeffs = [1, -10, -92, 234, 315]  # коэффициенты многочлена с целыми действительными корнями
coeffs = [1, -13, -121, -398, 386, -520]  # коэффициенты многочлена с комплексными смежными корнями
# coeffs = [1, 1, 1, 1, 1]  # коэффициенты многочлена с комплексными смежными корнями

n = len(coeffs) - 1  # степень многочлена
f_vector = np.zeros(n)  # начальный вектор f, после которого уже начинаем последовательный расчёт f для нахождения z1
f_vector[0] = 1  # задаём последний элемент единицей, чтобы везде не получились нули
f_history = f_vector


found_roots = []
found_groops = []
iter = 15
# делаем несколько итераций, чтобы приблизиться достаточно к корню.
# В представленном в книге примере 10 итераций достаточно.
# Берётся значение 15, чтобы всё-таки попробовать получить точность получше, так как
# для следующих колонок нужна большая тончость в предыдущих


f_vector = np.zeros (n)
# начальный вектор f, после которого уже начинаем последовательный расчёт f для нахождения z1
f_vector[0] = 1
# задаём последний элемент единицей, чтобы везде не получились нули
f_history = f_vector

for i in range (iter):
    f = push_f (f_vector, coeffs)
    f_history = np.insert (f_history, 0, push_f (f_vector, coeffs))
    f_vector = update_f (f, f_vector)

# print("Result after", iter, "iterations:\n", f_vector)
# print("x1: ", f_vector[0]/f_vector[1])
# отладочные выводы

found_roots.append (f_vector[0] / f_vector[1])
f_history = np.flip (f_history)

f_history = f_history[2:]
# эта строчка нужна, чтобы убрать f(-2) и f(-1), так как они больше не нужны для вычисления f_r(t)
# сделаем теперь f2
f2_history = []

fl_c = False  # флаг для того, чтобы вычислять корни другим методом (с косинусами)
# возьмём iter - 1 шагов, ведь нам придётся использовать величину на следующем шаге
for i in range(1, iter-1):
    f2_history.append((f_history[i]**2-f_history[i-1]*f_history[i+1]))
    if i > 3 and abs(f2_history[-1]-f2_history[-2]) > abs(f2_history[-2]-f2_history[-3]):
        # триггерится, когда столбец fr не сходится, то есть изменения по модулю больше чем на предыдущей итерации
        fl_c = True
        # продолжаем вычисления, так как столбец f2 нужен для вычисления c(t)

c_history = []
if(fl_c):
    print("-----------------------------------------")
    print("Встречен комплексный корень на столбце f2")
    print("-----------------------------------------")
    # сначала проводим шаг для определения Z3=z1*z2*z3=z1*r^2,
    # тем самым находим r.
    # несмотря на неправильность f2, Z3 должен сойтись
    frm2_history = f_history
    frm1_history = f2_history
    f3_history = []
    # возьмём iter - r шагов, ведь нам придётся использовать величину на следующем шаге
    for i in range (1, iter - 3 - 1):
        # здесь костыль, начинаем с 2 так как раньше были нули. пофикшу... потом
        # FIXME
        f3_history.append ((frm1_history[i] ** 2 - frm1_history[i - 1] * frm1_history[i + 1]) / frm2_history[i])

    Z3 = f3_history[-1]/f3_history[-2]
    Z1 = f_history[-1]/f_history[-2]
    print("Z3 =", Z3)
    print ("Z1 =", Z1)
    radius = np.sqrt(Z3/Z1)

    # ct_history = []
    # for i in range (2, iter - 3 - 1):
    #     c_history.append(f2_history[i]/f2_history/radius)
    #     if i > 2:
    #         ct_history.append(c_func(c_history[-2], c_history[-1]))
    print("-"*90)
    print("         Z2", "            c(t)", "              c(t+1)", "             (c(t)*c(t+1)+1) / (2*c(t))")
    for i in range(2, len(f2_history) - 2):
        Z2 = f2_history[i] / f2_history[i - 1]
        c = Z2 / radius / Z1  # c(t)
        ct = f2_history[i+1] / f2_history[i] / radius / Z1  # c(t+1)
        print(Z2, c, ct, c_func(c, ct))
    print("-"*90)
    cosine_value = c_func(c, ct)
    sine_value = sine(cosine_value)

    root1 = radius * (cosine_value + 1j * sine_value)
    root2 = radius * (cosine_value - 1j * sine_value)
    found_roots.append(root1)
    found_roots.append(root2)
    found_groops.append("unconverged")
    found_groops.append(Z3)
    print("radius", radius)
    print("found_roots", found_roots)
    # корни найдены. вынесено это отдельно затем,
    # что для первых двух столбцов f нахождение другое,
    # не деля на предыдущий определитель
    # далее будет реализовано уже в общем случае
else:
    # если не наткнулись на сопряженные комплексные корни
    print("-"*50)
    print ("t", "f(t)", "f2(t)")
    for i in range (0, len (f2_history)):
        if (i > 0) and (i < iter - 1):
            print (i, f_history[i], f2_history[i - 1])
        else:
            print (i, f_history[i])
    print ("-"*50)
    print ("x2*x1: ", f2_history[len (f2_history) - 1] / f2_history[len (f2_history) - 2])
    print ("x2: ", f2_history[len (f2_history) - 1] / f2_history[len (f2_history) - 2] / (
                f_history[len (f_history) - 1] / f_history[len (f_history) - 2]))
    found_roots.append (f2_history[len (f2_history) - 1] / f2_history[len (f2_history) - 2] / (
                f_history[len (f_history) - 1] / f_history[len (f_history) - 2]))
    found_groops.append (f2_history[len (f2_history) - 1] / f2_history[len (f2_history) - 2])


#
# # сделаем теперь f3-fn. здесь есть отличие - определитель нужно будет разделить на f2(t).
# # дальнейшие блоки итераций нет необходимости расписывать по-другому, только первые две
# frm1_history = f_history
# fr_history = f2_history
# for r in range(3, n+1):
#     frm2_history = frm1_history
#     frm1_history = fr_history
#     fr_history = []
#     print("r =", r)
#     print("frm2_history:", frm2_history)
#     print ("frm1_history:", frm1_history)
#     print ("fr_history:", fr_history)
#     # возьмём iter - r шагов, ведь нам придётся использовать величину на следующем шаге
#     for i in range (0, iter - r - 1):
#         # fr_history.append((f2_history[i]**2-f2_history[i-1]*f2_history[i+1])/f_history[i])
#         fr_history.append ((frm1_history[i] ** 2 - frm1_history[i - 1] * frm1_history[i + 1]) / frm2_history[i])
#     print ("Product of roots up to rth: ", fr_history[len (fr_history) - 1] / fr_history[len (fr_history) - 2])
#     found_groops.append(fr_history[len (fr_history) - 1] / fr_history[len (fr_history) - 2])
#     print ("Found root:", found_groops[len(found_groops)-1] / found_groops[len(found_groops)-2])
#     found_roots.append(found_groops[len(found_groops)-1] / found_groops[len(found_groops)-2])
#     print("Found groops:", found_groops)
# print("found roots:", found_roots)
#
