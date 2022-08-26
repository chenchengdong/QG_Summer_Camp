import copy

import numpy as np
import matplotlib.pyplot as plt
import random

def cricle(x0, x1, x_next, r):
    center = (x0 + x1) /2
    if np.linalg.norm(np.array([x_next[0] - center[0], x_next[1] - center[1]])) <= r:
        return True
    else:
        return False



def TpG(G,r_c):
    A_trad = np.zeros((np.shape(G)[1], np.shape(G)[1]))
    plt.cla()
    plt.figure(figsize=(4.5, 4.5))
    for i in range(np.shape(G)[1]):
        for j in range(np.shape(G)[1]):
            if ((G[0][j] - G[0][i])**2 + (G[1][j] - G[1][i])**2)**0.5 <= r_c and i != j:
                A_trad[i][j] = 1
                plt.plot([G[0][i], G[0][j]], [G[1][i], G[1][j]], c='b')
    plt.scatter(G[0], G[1], c='purple')
    plt.show()
    return A_trad

def rad(v, y0):
    if y0 > 0:
        return np.arccos(np.dot(v, np.array([1, 0]))/np.linalg.norm(v))
    else:
        return 2 * np.pi - np.arccos(np.dot(v, np.array([1, 0]))/np.linalg.norm(v))

def angle(v1, v2):
    return np.arccos(np.dot(v1, v2)/(np.linalg.norm(v1) *np.linalg.norm(v2)))

def farest_neighbour(section_neighbour, G, rank):
    if len(section_neighbour) == 0:
        return rank
    else:
        max_norm = 0.
        far_neighbour = rank
        for sn in section_neighbour:
            vector = np.array([G[0][sn]-G[0][rank], G[1][sn]-G[1][sn]])
            temp_norm = np.linalg.norm(vector)
            if temp_norm > max_norm:
                far_neighbour = sn
        return far_neighbour



def select(A_trad, G):
    final = []
    for i in range(len(A_trad)):
        Neighbour = np.nonzero(A_trad[i])[0]
        temp = {'N_1': [], 'N_2': [], 'N_3': [], 'N_4': []}
        for ne in Neighbour:
            v = np.array([G[0][ne] - G[0][i], G[1][ne] - G[1][i]])
            theta = rad(v, G[1][ne])
            if np.pi/2 * 0 <= theta < np.pi/2 * 1:
                temp['N_1'].append(ne)
            elif np.pi/2 * 1 <= theta < np.pi/2 * 2:
                temp['N_2'].append(ne)
            elif np.pi/2 * 2 <= theta < np.pi/2 * 3:
                temp['N_3'].append(ne)
            elif np.pi/2 * 3 <= theta < np.pi/2 * 4:
                temp['N_4'].append(ne)
        final.append(temp)
    return final

def SDB(A_trad, final, G):
    result = np.zeros((len(A_trad), len(A_trad)))
    for i in range(len(A_trad)):
        if sum(A_trad[i]) == len(A_trad) - 1:
            for index in range(len(A_trad[i])):
                if index != i:
                    result[i][index] = 1
        else:
            T = [0 if len(final[i]['N_1']) == 0 else 1,
                 0 if len(final[i]['N_2']) == 0 else 1,
                 0 if len(final[i]['N_3']) == 0 else 1,
                 0 if len(final[i]['N_4']) == 0 else 1]
            if np.dot(np.array(T), np.array([1, -1, 1, -1])) == 0 and sum(T) == 2:
                index_list = [index for index in range(len(T)) if T[index] != 0]
                choose_agent1 = i
                choose_agent2 = i
                num_dict = {'0': 'N_1', '1': 'N_2', '2': 'N_3', '3': 'N_4'}
                max_rad = 0
                for agent1 in final[i][num_dict[str(index_list[0])]]:
                    for agent2 in final[i][num_dict[str(index_list[1])]]:
                        rad_temp = angle(np.array([G[0][agent1]-G[0][i], G[1][agent1]-G[1][i]]), np.array([G[0][agent2]-G[0][i], G[1][agent2]-G[1][i]]))
                        if rad_temp > max_rad:
                            choose_agent1 = agent1
                            choose_agent2 = agent2
                cooperation = [choose_agent1, choose_agent2]
            else:
                cooperation = [farest_neighbour(final[i]['N_1'], G, i),
                               farest_neighbour(final[i]['N_1'], G, i),
                               farest_neighbour(final[i]['N_1'], G, i),
                               farest_neighbour(final[i]['N_1'], G, i)]
            for index in cooperation:
                if index != i:
                    result[i][index] = 1
    return result

def D(A_trad):
    return np.diag(np.sum(A_trad, axis=1))


def L(A_trad, D_trad):
    return A_trad - D_trad

def U_control(L_SDB, G, r_c, d):
    U = np.dot(L_SDB, G)
    U_hat = []
    for elem in U:
       U_hat.append(min((r_c-d)/(2*np.linalg.norm(elem)+1e-10), 1) * elem)
    return np.array(U_hat)

def A_id_f(A_trad, i, d, G):
    print('*进入A_id_f函数')
    I = [index for index in range(len(A_trad)) if A_trad[i][index] == 1]
    print('*'*50)
    print(f'i:{I}')
    A_id = np.zeros((len(I), len(I)))
    for num in range(len(I)):
        for index in range(len(I)):
            if np.linalg.norm(np.array([G[0][I[index]]-G[0][I[num]], G[1][I[index]]-G[1][I[num]]])) <= d and index != num:
                A_id[num][index] = 1
    return A_id

def component(A_id):
    result = []
    d_neighbour_list = [index for index in range(len(A_id))]
    while len(d_neighbour_list) != 0:
        print('1*'*50)
        print(d_neighbour_list)
        i = d_neighbour_list[0]
        temp_component = set([num for num in range(len(A_id)) if A_id[i][num] == 1])
        temp_component.add(i)
        temp1 = set([])
        print('2*'*50)
        print(temp_component)
        while not np.all(temp1 == temp_component):
            temp1 = temp_component
            for agent in range(len(A_id)):
                if not temp_component.isdisjoint(set([agent])):
                    temp2 = [num for num in range(len(A_id)) if A_id[agent][num] == 1]
                    temp_component = temp_component | set(temp2)
            print('3*'*50)
            print(list(temp_component))
        result.append(copy.deepcopy(list(temp_component)))
        print('5*'*50)
        print(temp_component)
        print(d_neighbour_list)
        for de in temp_component:
            d_neighbour_list.remove(de)
        print('*6'*50)
        print(d_neighbour_list)
    return result

def DP_i_f(A_trad, G, i, component_i):
    neighbours = [index for index in range(len(A_trad)) if A_trad[i][index] == 1]
    num = len(component_i)
    nearest_neighbour = []
    for nu in range(num):
        distance_min = 1000
        for index in component_i[nu]:
            distance_temp = np.linalg.norm(np.array([G[0][neighbours[index]]-G[0][i], G[1][neighbours[index]]-G[1][i]]))
            if distance_temp < distance_min:
                distance_min = distance_temp
                nearest_index = neighbours[index]
        nearest_neighbour.append(nearest_index)
    print('nearest')
    print(nearest_neighbour)
    return nearest_neighbour

def update(DP_i, G, i, X_hat, r_c):
    print('*进入update函数')
    lamuda = np.arange(1, 0, -0.01)
    max_lam = 0
    print(lamuda)
    for lam in lamuda:
        location_temp = (1-lam) * np.array([G[0][i], G[1][i]]) + lam * X_hat[i]
        print('*lam')
        print(lam)
        fall_in = np.array([cricle(np.array([G[0][i], G[1][i]]), np.array([G[0][elem], G[1][elem]]), location_temp, r_c/2) for elem in DP_i ])
        if np.any(fall_in):
            continue
        else:
            if lam > max_lam:
                max_lam = lam
    print('max_lam')
    print(max_lam)
    return (1-max_lam) * np.array([G[0][i], G[1][i]]) + max_lam * X_hat[i]

def count_lost(A_trad, G):
    lost = 0
    for i in range(len(A_trad)):
        temp = [((G[0][j] - G[0][i])**2 + (G[1][j] - G[1][i])**2) ** 0.5 for j in range(len(A_trad)) if j != i]
        lost += np.sum(temp)
    return lost

def fun_c(G, r_c, d):
    G_temp = np.array([[0, 0]])
    num = 0
    while not np.all((G.T - G_temp <= 1e-3)):
        num += 1
        G_temp = G.T
        A_trad_m = TpG(G, r_c)
        print('*' * 50)
        print(f'第{num}次循环')
        lost = count_lost(A_trad_m, G)
        print(f'损失值为:{lost}')
        final_m = select(A_trad_m, G)
        result_m = SDB(A_trad_m, final_m, G)
        D_m = D(result_m)
        L_m = L(result_m, D_m)
        U_hat_m = U_control(L_m, G.T, r_c, d)  # 跳过U，直接生成U_hat
        X_hat = G.T + U_hat_m
        for i in range(len(A_trad_m)):
            A_id_m = A_id_f(A_trad_m, i, d, G)
            component_i_m = component(A_id_m)
            DP_i_m = DP_i_f(A_trad_m, G, i, component_i_m)
            G.T[i] = update(DP_i_m, G, i, X_hat, r_c)



G = []
Gx = []
Gy = []
r_c = 1
d = 0.5
for i in range(300):
    Gx.append(random.uniform(-4, 4))
    Gy.append(random.uniform(-4, 4))
G = np.array([Gx, Gy])
fun_c(G, r_c, d)
# A_trad_m = TpG(G, r_c)
# print('*A_trad_m*')
# print(A_trad_m)
# final_m = select(A_trad_m, G)
# print('*final_m*')
# print(final_m)
# result_m = SDB(A_trad_m, final_m, G)
# print('*result*')
# print(result_m)
# D_m = D(result_m)
# L_m = L(result_m, D_m)
# print('*L_mat*')
# print(L_m)
# U_hat_m = U_control(L_m, G.T, r_c, d) #跳过U，直接生成U_hat
# print('*'*50)
# print(U_hat_m)
# X_hat = G.T + U_hat_m
# print('*'*50)
# print(X_hat)
# A_id_m = A_id_f(A_trad_m, 0, d, G)
# print('*'*50)
# print('A_id_m')
# print(A_id_m)
# component_i_m = component(A_id_m)
# print('*'*50)
# print('component')
# print(component_i_m)
# DP_i_m = DP_i_f(A_trad_m, G, 0, component_i_m)
# print('*'*50)
# print('DP_i')
# print(DP_i_m)
# x = update(DP_i_m, G, 0, X_hat, r_c)
# print('*'*50)
# print(x)













