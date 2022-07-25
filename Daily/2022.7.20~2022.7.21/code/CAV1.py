<<<<<<< HEAD
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

deta_t = 1e-4
gama = 1
beta = 1
times = int(10/deta_t)
flag = True

p_list = np.array([[6, 60], [10, 40], [16, 70]])
p_L = np.array([20., 50.])

v_list = np.array([[10, 5], [8, 4], [9, 3]])
v_L = np.array([6, 0], dtype="float")

# A = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) * 10
# D=np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]])*10
# L=D-A


A = np.ones((3, 3), dtype=int) * 5
D = np.zeros((3, 3), dtype=int)
if not flag:
    A[0, :] = 0
    A[:, 0] = 0
for i in range(3):
    A[i, i] = 0
for i in range(3):
    for j in range(3):
        D[i, i] += A[i, j]
L = D - A

r_list = np.array([[-15, 0], [-10, 0], [-5, 0]])
a_tem_list = np.zeros((3, 2))


p_tem_list = p_list
v_tem_list = v_list
p_final_list = []
v_final_list = []


p_final_list.append(np.vstack((p_tem_list, p_L)))
v_final_list.append(np.vstack((v_tem_list, v_L)))

K=np.array([[0, 0, 0], [0, 5, 0], [0, 0, 5]])


for m in range(times):
    a_tem_list = -np.dot(L, p_tem_list)+np.dot(L, r_list)-beta*np.dot(L, v_tem_list)-np.dot(K, (p_tem_list-p_L-r_list+v_tem_list-v_L))
    # 更新领导者速度
    p_L = p_L+deta_t*v_L
    v_tem_list = a_tem_list*deta_t+v_tem_list
    p_tem_list = p_tem_list+v_tem_list*deta_t
    v_final_list.append(np.vstack((v_tem_list, v_L)))
    p_final_list.append(np.vstack((p_tem_list, p_L)))

v_final_list = np.array(v_final_list)
p_final_list = np.array(p_final_list)

print(p_final_list)
color = ['red', 'green', 'blue', 'orange']
fig1 = plt.figure()



def gif1(i):
    # plt.legend()
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot([x[j, 0]for x in p_final_list[:i*500]], [y[j, 1]for y in p_final_list[:i*500]], c=c_)
        plt.annotate('', xytext=p_final_list[i*500][j, :], xy=p_final_list[i*500][j, :]+0.2*v_final_list[i*500][j, :],
                     arrowprops={'width': 1, 'headlength': 2, 'facecolor': c_})
    plt.ylabel('Y Position(m)')
    plt.xlabel('X Position(m)')
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower right')
    plt.tight_layout()
    plt.xlim((0, p_final_list[i*500][-1, 0]+5))
    plt.ylim(0, 80)


p_final_list = p_final_list[:-1]
a = len(p_final_list)
b = np.arange(0, a*deta_t, deta_t)


def gif2(i):
    if i == 0:
        return
    plt.cla()
    for j, c_ in zip(range(4), color):
        if j == 0:
            print("**")
            print(i)
            print(np.shape(np.linspace(0, min(i*500*deta_t, 10),
                                       len([(x[j, 0] - x[3, 0]) for x in p_final_list[:i*500]])))[0])
            print(len([(x[j, 0]-p_L[0]) for x in p_final_list[:i*500]]))

        lll = [(x[j, 0]-x[3, 0]) for x in p_final_list[:i*50]]
        # plt.plot(np.linspace(0,min(i*50*deta_t, 10),len([(x[j,0]-x[3,0]) for x in p_final_list[:i*50]])),
        # [(x[j,0]-x[3,0]) for x in p_final_list[:i*50]], c=c_)
        plt.plot(b[:i*500],
                 [(x[j, 0] - x[3, 0]) for x in p_final_list[:i * 500]], c=c_)
        # plt.annotate('', xytext=p_final_list[i * 10][j, :],
        #              xy=p_final_list[i * 500][j, :] + 0.2 * v_final_list[i * 500][j, :],
        #              arrowprops={'width': 1, 'headlength': 2, 'facecolor': c_})
    plt.ylim((-20, 5))
    plt.ylabel('Longitudinal Gap(m)')
    plt.xlabel('Time(s)' )
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower left')
    plt.tight_layout()


def gif3(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([(x[j, 1] - x[3, 1]) for x in p_final_list[:i * 500]])),
                 [(x[j, 1] - x[3, 1]) for x in p_final_list[:i * 500]], c=c_)

    plt.ylabel('Lateral Gap(m)')
    plt.xlabel('Time(s)')
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='upper right')
    plt.ylim(-10, 20)
    plt.tight_layout()


def gif4(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([v[j, 0] for v in v_final_list[:i*500]])),
                 [v[j, 0] for v in v_final_list[:i*500]])
        plt.ylabel('X-Velocity(m/s)')
        plt.xlabel('Time(s)')
        plt.ylim(-10, 12)
        plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='upper right')
        plt.tight_layout()


def gif5(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([v[j, 1]for v in v_final_list[:i*500]])),
                 [v[j, 1]for v in v_final_list[:i*500]], c=c_)
    plt.ylabel('Y-Velocity(m/s)')
    plt.xlabel('Time(s)')
    # plt.ylim(-10, 12)
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower right')
    plt.tight_layout()


if flag:
    animator1 = ani.FuncAnimation(fig1, gif1, interval=100)
    animator1.save('Fig4.gif' if flag else 'Fig7.gif')
if not flag:
    animator2 = ani.FuncAnimation(fig1, gif2, interval=100)
    animator2.save('Fig5(a).gif' if flag else 'Fig8(a).gif')
if not flag:
    animator3 = ani.FuncAnimation(fig1, gif3, interval=100)
    animator3.save('Fig5(b).gif' if flag else 'Fig8(b).gif')
if not flag:
    animator4 = ani.FuncAnimation(fig1, gif4, interval=100)
    animator4.save('Fig6(a).gif' if flag else 'Fig9(a).gif')
if not flag:
    animator5 = ani.FuncAnimation(fig1, gif5, interval=100)
=======
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

deta_t = 1e-4
gama = 1
beta = 1
times = int(10/deta_t)
flag = True

p_list = np.array([[6, 60], [10, 40], [16, 70]])
p_L = np.array([20., 50.])

v_list = np.array([[10, 5], [8, 4], [9, 3]])
v_L = np.array([6, 0], dtype="float")

# A = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) * 10
# D=np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]])*10
# L=D-A


A = np.ones((3, 3), dtype=int) * 5
D = np.zeros((3, 3), dtype=int)
if not flag:
    A[0, :] = 0
    A[:, 0] = 0
for i in range(3):
    A[i, i] = 0
for i in range(3):
    for j in range(3):
        D[i, i] += A[i, j]
L = D - A

r_list = np.array([[-15, 0], [-10, 0], [-5, 0]])
a_tem_list = np.zeros((3, 2))


p_tem_list = p_list
v_tem_list = v_list
p_final_list = []
v_final_list = []


p_final_list.append(np.vstack((p_tem_list, p_L)))
v_final_list.append(np.vstack((v_tem_list, v_L)))

K=np.array([[0, 0, 0], [0, 5, 0], [0, 0, 5]])


for m in range(times):
    a_tem_list = -np.dot(L, p_tem_list)+np.dot(L, r_list)-beta*np.dot(L, v_tem_list)-np.dot(K, (p_tem_list-p_L-r_list+v_tem_list-v_L))
    # 更新领导者速度
    p_L = p_L+deta_t*v_L
    v_tem_list = a_tem_list*deta_t+v_tem_list
    p_tem_list = p_tem_list+v_tem_list*deta_t
    v_final_list.append(np.vstack((v_tem_list, v_L)))
    p_final_list.append(np.vstack((p_tem_list, p_L)))

v_final_list = np.array(v_final_list)
p_final_list = np.array(p_final_list)

print(p_final_list)
color = ['red', 'green', 'blue', 'orange']
fig1 = plt.figure()



def gif1(i):
    # plt.legend()
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot([x[j, 0]for x in p_final_list[:i*500]], [y[j, 1]for y in p_final_list[:i*500]], c=c_)
        plt.annotate('', xytext=p_final_list[i*500][j, :], xy=p_final_list[i*500][j, :]+0.2*v_final_list[i*500][j, :],
                     arrowprops={'width': 1, 'headlength': 2, 'facecolor': c_})
    plt.ylabel('Y Position(m)')
    plt.xlabel('X Position(m)')
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower right')
    plt.tight_layout()
    plt.xlim((0, p_final_list[i*500][-1, 0]+5))
    plt.ylim(0, 80)


p_final_list = p_final_list[:-1]
a = len(p_final_list)
b = np.arange(0, a*deta_t, deta_t)


def gif2(i):
    if i == 0:
        return
    plt.cla()
    for j, c_ in zip(range(4), color):
        if j == 0:
            print("**")
            print(i)
            print(np.shape(np.linspace(0, min(i*500*deta_t, 10),
                                       len([(x[j, 0] - x[3, 0]) for x in p_final_list[:i*500]])))[0])
            print(len([(x[j, 0]-p_L[0]) for x in p_final_list[:i*500]]))

        lll = [(x[j, 0]-x[3, 0]) for x in p_final_list[:i*50]]
        # plt.plot(np.linspace(0,min(i*50*deta_t, 10),len([(x[j,0]-x[3,0]) for x in p_final_list[:i*50]])),
        # [(x[j,0]-x[3,0]) for x in p_final_list[:i*50]], c=c_)
        plt.plot(b[:i*500],
                 [(x[j, 0] - x[3, 0]) for x in p_final_list[:i * 500]], c=c_)
        # plt.annotate('', xytext=p_final_list[i * 10][j, :],
        #              xy=p_final_list[i * 500][j, :] + 0.2 * v_final_list[i * 500][j, :],
        #              arrowprops={'width': 1, 'headlength': 2, 'facecolor': c_})
    plt.ylim((-20, 5))
    plt.ylabel('Longitudinal Gap(m)')
    plt.xlabel('Time(s)' )
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower left')
    plt.tight_layout()


def gif3(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([(x[j, 1] - x[3, 1]) for x in p_final_list[:i * 500]])),
                 [(x[j, 1] - x[3, 1]) for x in p_final_list[:i * 500]], c=c_)

    plt.ylabel('Lateral Gap(m)')
    plt.xlabel('Time(s)')
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='upper right')
    plt.ylim(-10, 20)
    plt.tight_layout()


def gif4(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([v[j, 0] for v in v_final_list[:i*500]])),
                 [v[j, 0] for v in v_final_list[:i*500]])
        plt.ylabel('X-Velocity(m/s)')
        plt.xlabel('Time(s)')
        plt.ylim(-10, 12)
        plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='upper right')
        plt.tight_layout()


def gif5(i):
    plt.cla()
    for j, c_ in zip(range(4), color):
        plt.plot(np.linspace(0, min(i*500*deta_t, 10), len([v[j, 1]for v in v_final_list[:i*500]])),
                 [v[j, 1]for v in v_final_list[:i*500]], c=c_)
    plt.ylabel('Y-Velocity(m/s)')
    plt.xlabel('Time(s)')
    # plt.ylim(-10, 12)
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"], loc='lower right')
    plt.tight_layout()


if flag:
    animator1 = ani.FuncAnimation(fig1, gif1, interval=100)
    animator1.save('Fig4.gif' if flag else 'Fig7.gif')
if not flag:
    animator2 = ani.FuncAnimation(fig1, gif2, interval=100)
    animator2.save('Fig5(a).gif' if flag else 'Fig8(a).gif')
if not flag:
    animator3 = ani.FuncAnimation(fig1, gif3, interval=100)
    animator3.save('Fig5(b).gif' if flag else 'Fig8(b).gif')
if not flag:
    animator4 = ani.FuncAnimation(fig1, gif4, interval=100)
    animator4.save('Fig6(a).gif' if flag else 'Fig9(a).gif')
if not flag:
    animator5 = ani.FuncAnimation(fig1, gif5, interval=100)
>>>>>>> b4f752a (add files)
    animator5.save('Fig6(b).gif' if flag else 'Fig9(b).gif')