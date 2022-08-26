import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
deta_t=1e-4
gama=1
beta=1
times=int(10/deta_t)

p_list=np.array([[6,60],[10,40],[16,70]])
p_L=np.array([20.,50.])

v_list=np.array([[10,5],[8,4],[9,3]])
v_L=np.array([6.,0.])

A=np.array([[0,1,1],[1,0,1],[1,1,0]])*10
D=np.array([[2,0,0],[0,2,0],[0,0,2]])*10
L=D-A


r_list=np.array([[-15,0],[-10,0],[-5,0]])
a_tem_list=np.zeros((3,2))


p_tem_list=p_list
v_tem_list=v_list
p_final_list=[]
v_final_list=[]


p_final_list.append(np.vstack((p_tem_list,p_L)))
v_final_list.append(np.vstack((v_tem_list,v_L)))

K=np.array([[0,0,0],[0,10,0],[0,0,10]])


for m in range(times):
    a_tem_list=-np.dot(L,p_tem_list)+np.dot(L,r_list)-beta*np.dot(L,v_tem_list)-np.dot(K,(p_tem_list-p_L-r_list+v_tem_list-v_L))
    p_L=p_L+deta_t*v_L       #更新领导者速度
    v_tem_list=a_tem_list*deta_t+v_tem_list
    p_tem_list=p_tem_list+v_tem_list*deta_t
    v_final_list.append(np.vstack((v_tem_list,v_L)))
    p_final_list.append(np.vstack((p_tem_list,p_L)))

v_final_list=np.array(v_final_list)
p_final_list=np.array(p_final_list)

print(p_final_list)
color=['red','green','blue','orange']
fig=plt.figure()


def gif1(i=int):
    # plt.legend()
    plt.cla()
    for j,c_ in zip(range(4),color):
        plt.plot([x[j,0]for x in p_final_list[:i*500]],[y[j,1]for y in p_final_list[:i*500]],c=c_)
        plt.annotate('',xytext=p_final_list[i*500][j,:], xy=p_final_list[i*500][j,:]+0.2*v_final_list[i*500][j,:], arrowprops={'width':1,'headlength':2,'facecolor':c_})
    plt.ylabel('Y Position(m)')
    plt.xlabel('X Position(m)')
    plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"])
    plt.tight_layout()
    plt.xlim((0, p_final_list[i*500][-1,0]+5))


# def gif2(i=int):
#     plt.cla()
#     for j,c_ in zip(range(4),color):
#         plt.plot([(x[j,0]-p_L[0,0]) for x in p_final_list[:i*500]],range(0,10.0,0.02),c=c_)
#     plt.ylim((-20,5))
#     plt.tight_layout()
#     plt.ylabel('Longitudinal Gap(m)')
#     plt.xlabel('Time(s)')
#     plt.legend(["Vehicle i", "Vehicle i+1", "Vehicle i+2", "Leader"])

animator=ani.FuncAnimation(fig, gif1, interval=100)
animator.save('picture1.gif')

