import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani


deta_t = 1e-3
times = int(12 / deta_t)

PL1 = np.array([80, 1])
PL2 = np.array([30, 2])
VL1 = np.array([10, 0])
VL2 = np.array([10, 0])
p1_list = np.array([[70, 1], [60, 1]])
p2_list = np.array([[20, 2], [10, 2]])
v1_list = np.array([[10, 0], [10, 0]])
v2_list = np.array([[10, 0], [10, 0]])
R1_list = np.array([[-10, 0], [-20, 0]])
R2_list = np.array([[-10, 0], [-20, 0]])
RLL = np.array([-30, 0])
RLLF2 = np.array([-10, 0])

V1X_tem = v1_list[:, 0].reshape(2, 1)
V1Y_tem = v1_list[:, 1].reshape(2, 1)
V2X_tem = v2_list[:, 0].reshape(2, 1)
V2Y_tem = v2_list[:, 1].reshape(2, 1)
VL2X_tem = VL2[0]
VL2Y_tem = VL2[1]

P1X_tem = p1_list[:, 0].reshape(2, 1)
P1Y_tem = p1_list[:, 1].reshape(2, 1)
P2X_tem = p2_list[:, 0].reshape(2, 1)
P2Y_tem = p2_list[:, 1].reshape(2, 1)
PL2X_tem = PL2[0]
PL2Y_tem = PL2[1]


p_final_list = []
v_final_list = []

p_final_list.append(np.vstack((np.vstack((p1_list, p2_list)), np.vstack((PL1, PL2)))))
v_final_list.append(np.vstack((np.vstack((v1_list, v2_list)), np.vstack((VL1, VL2)))))

for i in range(times):
    # print(P1X_tem-PL1[0]-R1_list[:, 0].reshape(2, 1)+V1X_tem-VL1[0])
    A1X_tem = - (P1X_tem-PL1[0]-R1_list[:, 0].reshape(2, 1)+V1X_tem-VL1[0]) - (np.vstack((0, P1X_tem[1]-PL2[0]+RLLF2[0]+V1X_tem[1]-VL2[0])))
    A2X_tem = - (P2X_tem-PL2[0]-R2_list[:, 0].reshape(2, 1)+V2X_tem-VL2[0])
    print('*')
    # print(P1Y_tem[:, 1])
    # print(PL1[1].shape)
    # print(R1_list[:, 1].shape)
    # print(V1Y_tem[:, 1].shape)
    # print(VL1[1].shape)
    print(V1X_tem[1, 0])
    A1Y_tem = -10 * (P1Y_tem-PL1[1]-R1_list[:, 1].reshape(2, 1)+V1Y_tem-VL1[1])
    A2Y_tem = -10 * (P2Y_tem-PL2[1]-R2_list[:, 1].reshape(2, 1)+V2Y_tem-VL2[1])
    AL2X_tem = - (PL2[0]-PL1[0]-RLL[0]) - (VL2[0]-VL1[0]) - (PL2[0]-P1X_tem[1]-RLLF2[0]) - (VL2[0]-V1X_tem[1])
    AL2Y_tem = -5 * (PL2[1]-PL1[1]-RLL[1]) - 5 * (VL2[1]-VL1[1])
    print(AL2X_tem)
    V1X_tem = V1X_tem + A1X_tem * deta_t
    V1Y_tem = V1Y_tem + A1Y_tem * deta_t

    V2X_tem = V2X_tem + A2X_tem * deta_t
    V2Y_tem = V2Y_tem + A2Y_tem * deta_t
    VL2X_tem = VL2X_tem + AL2X_tem * deta_t
    VL2Y_tem = VL2Y_tem + AL2Y_tem * deta_t
    VL2 = np.hstack((VL2X_tem, VL2Y_tem))
    print(VL2)


    P1X_tem = P1X_tem + V1X_tem * deta_t
    P1Y_tem = P1Y_tem + V1Y_tem * deta_t
    P2X_tem = P2X_tem + V2X_tem * deta_t
    P2Y_tem = P2Y_tem + V2Y_tem * deta_t
    PL2X_tem = PL2X_tem + VL2X_tem * deta_t
    PL2Y_tem = PL2Y_tem + VL2Y_tem * deta_t
    PL2 = np.hstack((PL2X_tem, PL2Y_tem))

    PL1 = PL1 + VL1*deta_t
    print('**')
    # print(V1X_tem)
    print(np.vstack((np.vstack((np.hstack((V1X_tem, V1Y_tem)), np.hstack((V2X_tem, V2Y_tem)))), np.vstack((VL1, VL2)))))
    v_final_list.append(np.vstack((np.vstack((np.hstack((V1X_tem, V1Y_tem)), np.hstack((V2X_tem, V2Y_tem)))), np.vstack((VL1, VL2)))))
    p_final_list.append(np.vstack((np.vstack((np.hstack((P1X_tem, P1Y_tem)), np.hstack((P2X_tem, P2Y_tem)))), np.vstack((PL1, PL2)))))


color = ['red', 'green', 'blue', 'orange', 'yellow', 'pink']
fig1 = plt.figure()


def gif(i):
    plt.cla()
    for j, c_ in zip(range(6), color):
        plt.plot([x[j, 0]for x in p_final_list[:i*200]], [y[j, 1]for y in p_final_list[:i*200]], c=c_)
        plt.xlabel('X位置/m')
        plt.ylabel('Y位置/m')
        plt.legend(['follower1', 'follower2', 'follower3', 'follower4', 'leader1', 'leader2'], loc='upper right')
        plt.ylim(0, 2.5)
        plt.xlim(0, 200)
        plt.tight_layout()


animator = ani.FuncAnimation(fig1, gif, interval=100)
plt.show()

# for j, c_ in zip(range(6), color):
#     plt.plot([x[j, 0] for x in p_final_list], [y[j, 1] for y in p_final_list], c=c_)
#
# plt.show()









