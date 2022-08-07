import numpy as np
import matplotlib.pyplot as plt
import copy
import matplotlib.animation as ani

deta_t = 1e-3
times = int(10/deta_t)
yita1 = 0.05014
yita2 = 0.02733
yita3 = 0.05915
pai = 1
gama1 = 1
gama2 = 1
gama3 = 10
gama4 = 10

# A = np.mat([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]])
# print(np.diag(A.sum(axis=1)))
# print(A)
# L = np.diag(A.sum(axis=1)) - A
# print(L)
L = np.mat([[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]])

x = np.mat([[18, 1], [12, 1], [8, 1], [0, 1], [15, 3], [11, 3], [5, 3], [0, 3]], dtype=float)
v = np.mat([[4.8, 0], [5.2, 0], [4.9, 0], [5.1, 0], [6.0, 0], [6.2, 0], [5.8, 0], [6.1, 0]], dtype=float)
e = np.mat([[-5, 1], [-10, 1], [-15, 1], [-20, 1], [-5, 3], [-10, 3], [-15, 3], [-20, 3]], dtype=float)
x_l, v_l, e_l = np.mat([23., 1]), np.mat([5.1, 0]), np.mat([0, 1.])
x_f, v_f, e_f = np.mat([20., 3]), np.mat([5.8, 0]), np.mat([0, 3.])
E_1 = - np.dot(L, e[:4, :])
E_2 = - np.dot(L, e[4:, :])
E_L = e_l - e_f
_list_x1 = []
_list_x2 = []
_list_v1 = []
_list_v2 = []
_list_xl = []
_list_xf = []
_list_vf = []


def update_cars(x,  v,  e, L_mat, ci, vl, xl, el):
    for c, j in zip(ci, range(x.shape[0])):
        if c > 0:
            a = -(gama1 * (np.dot(L_mat[j, :], x)) - gama2 *(np.dot(L_mat[j, :], e)) + np.dot(L_mat[j, :], v)) \
                - pai * (gama3 * (x[j, :] - xl - (e[j, :] - el)) +gama4 * (v[j, :] - vl))
            v[j, :] += a*deta_t
            x[j, :] += v[j, :]*deta_t
        else:
            x[j, :] += v[j, :]*deta_t
    return x, v


def condition(x, v, L_mat):
    qi = - np.dot(L_mat, x) - np.dot(L_mat, v)
    return qi


def controller(E, q, yita):
    ci = np.sqrt(np.square(E-q).sum(axis=1)) - yita * np.sqrt(np.square(q).sum(axis=1))
    return ci


for i in range(times):
    #   更新主领导车
    x_l += v_l * deta_t
    _list_xl.append(copy.deepcopy(x_l))
    #   更新从领导车
    qi_L = -(x_l - x_f) - (v_l - v_f)
    c_L = np.sqrt(np.square(E_L - qi_L).sum(axis=1)) - np.sqrt(np.square(qi_L).sum(axis=1))
    if c_L > 0:
        a_L = - (x_f - x_l - (e_f - e_l) + (v_f - v_l))
        v_f += a_L*deta_t
        x_f += v_f * deta_t
        _list_vf.append(copy.deepcopy(v_f))
        _list_xf.append(copy.deepcopy(x_f))
    qi1 = condition(x[:4, :], v[:4, :], L)
    c_1 = controller(E_1, qi1, yita1)
    x[:4, :], v[:4, :] = update_cars(x[:4, :], v[:4, :], e[:4, :], L, c_1, v_l, x_l, e_l)
    _list_x1.append(copy.deepcopy(x[:4, :]))
    _list_v1.append(copy.deepcopy(v[:4, :]))
    qi2 = condition(x[4:, :], v[4:, :], L)
    c_2 = controller(E_2, qi2, yita1)
    x[4:, :], v[4:, :] = update_cars(x[4:, :], v[4:, :], e[4:, :], L, c_2, v_f, x_f, e_f)
    _list_x2.append(copy.deepcopy(x[4:, :]))
    _list_v2.append(copy.deepcopy(v[4:, :]))



ne1 = []
ne2 = []
leader1, leader2 = 1, 2
_list_a = [2, 2, 2, 1]
_list_b = [2, 1, 2, 1]
e[:4, :] -= e_l
e[4:, :] -= e_f
# k = 1
# while k:
#     k = 0
#     for i in range(4):
#         a = 0
#         for j in _list_b[:i+1]:
#             if j == leader1:
#                 a += 1
#         if _list_b[i] != leader1:
#             e[i, :] = (a * e[i, :])/(i+1) + e[i, :]
#         else:
#             e[i, :] = ((a+1) * e[i, :])/(i+1) + e[i, :]
#     for i in range(4):
#         if _list_a[i] == leader2:
#             if e[i, 0] == e[i+4, 0]:
#                 e[i+4:, :] += e[i+4:, :]/(i+1)
#             else:
#                 e[i+4, :] = e[i+4, :]
# e[:4, 1] = 1
# e[4:, 1] = 3
e = np.mat([[-5, 1], [-15, 1], [-25, 1], [-30, 1], [-10, 3], [-20, 3], [-30, 3], [-35, 3]])
print(e)

E_1 = - np.dot(L, e[:4, :])
E_2 = - np.dot(L, e[4:, :])

for i in range(times):
    #   更新主领导车
    x_l += v_l * deta_t
    _list_xl.append(copy.deepcopy(x_l))
    #   更新从领导车
    qi_L = -(x_l - x_f) - (v_l - v_f)
    c_L = np.sqrt(np.square(E_L - qi_L).sum(axis=1)) - np.sqrt(np.square(qi_L).sum(axis=1))
    if c_L > 0:
        a_L = - (x_f - x_l - (e_f - e_l) + (v_f - v_l))
        v_f += a_L*deta_t
        x_f += v_f * deta_t
        _list_vf.append(copy.deepcopy(v_f))
        _list_xf.append(copy.deepcopy(x_f))
    qi1 = condition(x[:4, :], v[:4, :], L)
    c_1 = controller(E_1, qi1, yita1)
    x[:4, :], v[:4, :] = update_cars(x[:4, :], v[:4, :], e[:4, :], L, c_1, v_l, x_l, e_l)
    _list_x1.append(copy.deepcopy(x[:4, :]))
    _list_v1.append(copy.deepcopy(v[:4, :]))
    qi2 = condition(x[4:, :], v[4:, :], L)
    c_2 = controller(E_2, qi2, yita1)
    x[4:, :], v[4:, :] = update_cars(x[4:, :], v[4:, :], e[4:, :], L, c_2, v_f, x_f, e_f)
    _list_x2.append(copy.deepcopy(x[4:, :]))
    _list_v2.append(copy.deepcopy(v[4:, :]))


v = np.array(v)
x = np.array(x)
e = np.array(e)

L1 = np.mat([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
L2 = np.mat([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
L3 = np.mat([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
L4 = np.mat([[1, -1, 0, 0, 0], [-1, 2, -1, 0, 0], [0, -1, 2, -1, 0], [0, 0, -1, 2, -1], [0, 0, 0, -1, 1]])
v1 = np.mat([v[5, :], v[3, :], v[7, :]])
v2 = np.mat([v[0, :], v[4, :], v[1, :], v[2, :], v[6, :]])
x1 = np.mat([x[5, :], x[3, :], x[7, :]])
x2 = np.mat([x[0, :], x[4, :], x[1, :], x[2, :], x[6, :]])
e1 = np.mat([e[5, :], e[3, :], e[7, :]])
e1[:, 1] = 1

e2 = np.mat([e[0, :], e[4, :], e[1, :], e[2, :], e[6, :]])
e2[:, 1] = 3
print(x2)
print(e2)
E_1 = - np.dot(L3, e1)
E_2 = - np.dot(L4, e2)
E_L = e_l - e_f

_list_x11 = []
_list_v11 = []
_list_x22 = []
_list_v22 = []

for i in range(times):
    #   更新主领导车
    x_l += v_l * deta_t
    _list_xl.append(copy.deepcopy(x_l))
    #   更新从领导车
    qi_L = -(x_l - x_f) - (v_l - v_f)
    c_L = np.sqrt(np.square(E_L - qi_L).sum(axis=1)) - np.sqrt(np.square(qi_L).sum(axis=1))
    if c_L > 0:
        a_L = - (x_f - x_l - (e_f - e_l) + 1 * (v_f - v_l))
        v_f += a_L*deta_t
        x_f += v_f * deta_t
        _list_vf.append(copy.deepcopy(v_f))
        _list_xf.append(copy.deepcopy(x_f))
    qi1 = condition(x1, v1, L1)
    c_1 = controller(E_1, qi1, yita2)
    x1, v1 = update_cars(x1, v1, e1, L1, c_1, v_l, x_l, e_l)
    _list_x11.append(copy.deepcopy(x1))
    _list_v11.append(copy.deepcopy(v1))
    qi2 = condition(x2, v2, L2)
    c_2 = controller(E_2, qi2, yita3)
    x2, v2 = update_cars(x2, v2, e2, L2, c_2, v_f, x_f, e_f)
    _list_x22.append(copy.deepcopy(x2))
    _list_v22.append(copy.deepcopy(v2))


e1 = np.mat([[-5, 1], [-10, 1], [-15, 1]])
e2 = np.mat([[-5, 3], [-10, 3], [-15, 3], [-20, 3], [-25, 3]])

E_1 = - np.dot(L3, e1)
E_2 = - np.dot(L4, e2)

for i in range(times):
    #   更新主领导车
    x_l += v_l * deta_t
    _list_xl.append(copy.deepcopy(x_l))
    #   更新从领导车
    qi_L = -(x_l - x_f) - (v_l - v_f)
    c_L = np.sqrt(np.square(E_L - qi_L).sum(axis=1)) - np.sqrt(np.square(qi_L).sum(axis=1))
    if c_L > 0:
        a_L = - (x_f - x_l - (e_f - e_l) + 10* (v_f - v_l))
        v_f += a_L*deta_t
        x_f += v_f * deta_t
        _list_vf.append(copy.deepcopy(v_f))
        _list_xf.append(copy.deepcopy(x_f))
    qi1 = condition(x1, v1, L3)
    c_1 = controller(E_1, qi1, yita2)
    x1, v1 = update_cars(x1, v1, e1, L3, c_1, v_l, x_l, e_l)
    _list_x11.append(copy.deepcopy(x1))
    _list_v11.append(copy.deepcopy(v1))
    qi2 = condition(x2, v2, L4)
    c_2 = controller(E_2, qi2, yita3)
    x2, v2 = update_cars(x2, v2, e2, L4, c_2, v_f, x_f, e_f)
    _list_x22.append(copy.deepcopy(x2))
    _list_v22.append(copy.deepcopy(v2))


for xx1, vv1, xx2, vv2 in zip(_list_x11, _list_v11, _list_x22, _list_v22):
    xx1 = np.array(xx1)
    xx2 = np.array(xx2)
    vv1 = np.array(vv1)
    vv2 = np.array(vv2)
    tem_x1 = np.mat([xx2[0, :], xx2[2, :], xx2[3, :], xx1[1, :]])
    tem_x2 = np.mat([xx2[1, :], xx1[0, :], xx2[4, :], xx1[2, :]])
    tem_v1 = np.mat([vv2[0, :], vv2[2, :], vv2[3, :], vv1[1, :]])
    tem_v2 = np.mat([vv2[1, :], vv1[0, :], vv2[4, :], vv1[2, :]])
    _list_x1.append(copy.deepcopy(tem_x1))
    _list_x2.append(copy.deepcopy(tem_x2))
    _list_v1.append(copy.deepcopy(tem_v1))
    _list_v2.append(copy.deepcopy(tem_v2))


colorf = ['red', 'blue', 'yellow', 'black', 'green', 'brown', 'purple', 'pink', 'orange', 'yellowgreen']
_list_xfinal = []
_list_vfinal = []
fig1 = plt.figure()
for lea1, lea2, x1, x2 in zip(_list_xl, _list_xf, _list_x1, _list_x2):
    tem1 = np.vstack((lea1, lea2))
    tem2 = np.vstack((x1, x2))
    _list_xfinal.append(np.vstack((tem1, tem2)))

for lea2, v1, v2 in zip(_list_vf, _list_v1, _list_v2):
    tem2 = np.vstack((v1, v2))
    _list_vfinal.append(np.vstack((lea2, tem2)))


def gif1(i):
    plt.cla()
    for j, c_ in zip(range(len(colorf)), colorf):
        plt.plot([x[j, 0] for x in _list_xfinal[:i * 200]], [y[j, 1] for y in _list_xfinal[:i * 200]], c=c_)
        if j == 0:
            plt.annotate('', xy=tuple(np.array(_list_xfinal[i*200])[j, :]+0.2*np.array(v_l)[0]),
                         xytext=tuple(np.array(_list_xfinal[i*200])[j, :]),
                         arrowprops={'width': 5, 'headlength': 10, 'facecolor': c_, 'shrink':2})

        else:
            plt.annotate('', xy=tuple(np.array(_list_xfinal[i*200])[j, :]+0.2*np.array(_list_vfinal[i*200])[j-1, :]),
                         xytext=tuple(np.array(_list_xfinal[i*200])[j, :]),
                         arrowprops={'width': 5, 'headlength': 10, 'facecolor': c_,'shrink':2})

    plt.ylabel('Y')
    plt.xlabel('X')
    # plt.legend(["Leader1", "Leader2", "Vehicle1", "Vehicle2",
    #             "Vehicle3","Vehicle4","Vehicle5","Vehicle6","Vehicle7","Vehicle8"], loc='best')
    plt.ylim((0.5, 3.5))
    plt.tight_layout()
for i in range(10):
    plt.plot([x[i, 0] for x in _list_xfinal])
plt.show()
fig1 = plt.figure()
an = ani.FuncAnimation(fig1, gif1, interval=100, save_count=500)
an.save('gif1.gif')
plt.show()