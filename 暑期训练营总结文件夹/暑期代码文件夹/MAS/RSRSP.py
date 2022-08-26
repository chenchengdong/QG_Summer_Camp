import numpy as np
import matplotlib.pyplot as plt
import copy


def cir(x0, y0, R):
    if (x0 - 0)**2 + (y0 - 0)**2 <= R**2:
        return True
    else:
        return False


def A(G, r_c, times, save_file, show_flag=False, save_flag=True):
    A_trad = np.zeros((np.shape(G)[1], np.shape(G)[1]), dtype=int)
    fig1 = plt.figure(figsize=(4, 4))
    plt.xlim((-4, 4))
    plt.ylim((-4, 4))
    for i in range(len(A_trad)):
        for j in range(len(A_trad)):
            if ((G[0][j] - G[0][i])**2 + (G[1][j] - G[1][i])**2)**0.5 <= r_c and j != i:
                A_trad[i][j] = 1
                if times % 20 == 0:
                    plt.plot([G[0][i], G[0][j]], [G[1][i], G[1][j]], c='k', linewidth=0.5)

    if show_flag:
        plt.show()
    if save_flag:
        if times % 20 == 0:
            plt.scatter(G[0], G[1], c='b')
            plt.savefig(save_file + f'pic{times}' + '.png')
    return A_trad

# def token(A_trad):
#     arr_token = np.zeros((len(A_trad), len(A_trad)), dtype=int)
#     for i in range(len(A_trad)):
#         if len(A_trad[i].nonzero()[0]) != len(A_trad) - 1:
#             arr_token[i][i] = 0
#         else:
#



def span(G, i, N, theta):
    x_axis = np.array([np.cos(theta), np.sin(theta)])
    # print('*'*50)
    # print(f'theta:{theta} cos_theta:{np.cos(theta)} sin_theta:{np.sin(theta)}')
    temp = {'N_1': [], 'N_2': [], 'N_3': [], 'N_4': []}
    for Nei in N:
        vector = np.array([G[0][Nei] - G[0][i], G[1][Nei] - G[1][i]])
        if vector[1] > 0:
            theta_tem = np.arccos(np.dot(vector, x_axis) / (np.linalg.norm(vector) * np.linalg.norm(x_axis)))
        else:
            theta_tem = 2*np.pi - np.arccos(np.dot(vector, x_axis) / (np.linalg.norm(vector) * np.linalg.norm(x_axis)))
        if (np.pi/2 * 0 + theta) <= theta_tem < (np.pi/2 * 1 + theta):
            temp['N_1'].append(Nei)
        elif (np.pi/2 * 1 + theta) <= theta_tem < (np.pi/2 * 2 + theta):
            temp['N_2'].append(Nei)
        elif (np.pi/2 * 2 + theta) <= theta_tem < (np.pi/2 * 3 + theta):
            temp['N_3'].append(Nei)
        elif (np.pi/2 * 3 + theta) <= theta_tem < (np.pi/2 * 4 + theta):
            temp['N_4'].append(Nei)
    return temp

def cla_update(L_trad, GT, alpha2):
    return (GT + alpha2 * np.dot(L_trad, GT)).T

def select(G, A_trad):
    names = ['N_1', 'N_2', 'N_3', 'N_4']
    sel = []
    for i in range(len(A_trad)):
        Neighbour = [index for elem, index in zip(A_trad[i], range(len(A_trad))) if elem != 0]
        aver_N = round(len(Neighbour)/4)
        variance_min = 10000
        dict_tem = {}
        dict_index = 0
        for j in range(90):
            theta = (j/360) * np.pi*2
            temp = span(G, i, Neighbour, theta)
            # print('@'*50)
            # print(f'第{j+1}次划分区域')
            variance_temp = 0
            for na in names:
                variance_temp += ((len(temp[na]) - aver_N)**2)/4
            if variance_temp < variance_min:
                variance_min = variance_temp
                # print(f'第{i}个智能体第{j}次划分的总方差：{variance_min}')
                dict_tem = temp
                dict_index = j + 1

        # print('%'*50)
        # print(f'最终选择了第{dict_index}次划分的扇区')
        # print('&'*50)
        # print(f'最终分扇区情况：{dict_tem}, 平均为每个扇区：{aver_N}个点')
        sel.append(copy.deepcopy(dict_tem))
    return sel

def sent(sel, G, A_trad):
    names = {'N_1': [], 'N_2': [], 'N_3': [], 'N_4': []}
    A_ik = np.zeros((len(A_trad), len(A_trad)), dtype=int)
    for i in range(len(A_trad)):
        for na in names:
            distance_min = 10000
            if len(sel[i][na]) == 0:
                continue
            else:
                index_min = 0
                for index in sel[i][na]:
                    distance_temp = ((G[0][index] - G[0][i])**2 + (G[1][index] - G[1][i])**2)**0.5
                    if distance_temp <= distance_min:
                        distance_min = distance_temp
                        index_min = index
                A_ik[i][index_min] = 1
    return A_ik


def receive(A_left, A_ik):
    P_ik = np.zeros((len(A_left), len(A_left)), dtype=int)
    for i in range(len(A_left)):
        shorten_neighbour = np.nonzero(A_left[i])[0]
        for sh_ne in shorten_neighbour:
            temp = np.nonzero(A_ik[sh_ne])[0]
            for index in temp:
                if index == i:
                    P_ik[i][sh_ne] = 1
    return P_ik

def D(A_trad):
    D_trad = np.diag(np.sum(A_trad, axis=1))
    return D_trad


def L_ji(A_trad, D_trad):
    L_trad = A_trad - D_trad
    return  L_trad

def U_ji(L_A_ik, L_P_ik, GT):
    U_rsrsp = np.dot(L_A_ik, GT) + np.dot(L_P_ik, GT)
    return U_rsrsp


def update(GT, U_rsrsp, alpha):
    return (GT + alpha * U_rsrsp).T

def count_lost(A_trad, G):
    lost = 0
    for i in range(len(A_trad)):
        temp = [((G[0][j] - G[0][i])**2 + (G[1][j] - G[1][i])**2) ** 0.5 for j in range(len(A_trad)) if j != i]
        lost += np.sum(temp)
    return lost

def to_sql():
    pass

def RSRSP(G, r_c):
    lost = 10000
    times = 1
    save_file = 'E:/lecture/8.15img/'
    # final_location = []
    # final_adjacency = []
    while lost >= 10:
        G_temp = G.T
        A_m = A(G, r_c, times, save_file=save_file, show_flag=False, save_flag=True)
        lost = count_lost(A_m, G)
        print('*' * 50)
        print(f'第{times}次循环')
        print(f'损失值为:{lost}')
        times += 1
        A_compare = np.ones((len(A_m), len(A_m)), dtype=int)
        np.fill_diagonal(A_compare, np.diag(np.diagonal(A_m)))
        if np.all(A_compare == A_m):
            # print('*'*50)
            print('SAN')
            D_A_ik_m = D(A_m)
            L_A_ik_m = L_ji(A_m, D_A_ik_m)
            G = cla_update(L_A_ik_m, G_temp, alpha2)
            continue
        else:
            # print('*'*50)
            print('RSRSP')
            sel_m = select(G, A_m)
            A_ik_m = sent(sel_m, G, A_m)
            A_left_m = A_m - A_ik_m
            P_ik_m = receive(A_left_m, A_ik_m)
            D_A_ik_m = D(A_ik_m)
            D_P_ik_m = D(P_ik_m)
            L_A_ik_m = L_ji(A_ik_m, D_A_ik_m)
            L_P_ik_m = L_ji(P_ik_m, D_P_ik_m)
            U_m = U_ji(L_A_ik_m, L_P_ik_m, G_temp)
            G = update(G_temp, U_m, alpha1)





G = []
Gx = []
Gy = []
r_c = 0.5
# while len(Gx) != 120:
#         x0 = np.random.uniform(-3, 3)
#         y0 = np.random.uniform(-3, 3)
#         print(x0)
#         if len(Gx) == 0:
#             if cir(x0, y0, 3):
#                 Gx.append(x0)
#                 Gy.append(y0)
#         else:
#             if np.any(np.array(Gx) != x0):
#                 if cir(x0, y0, 3):
#                     Gx.append(x0)
#                     Gy.append(y0)
#
#         print(Gx)

# G = np.array([Gx, Gy])
G = np.load(r'E:\lecture\8.15\001log_uniform_200.npy')
G = G.T
alpha1 = 0.1
alpha2 = 0.01
RSRSP(G, r_c)






















