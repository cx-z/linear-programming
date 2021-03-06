# -*- coding:utf-8 -*-
import numpy,random,pulp


class edge:
    def __init__(self,src,dst,cap):
        self.src = src  #源节点
        self.dst = dst  #目的节点
        self.cap = cap  #链路容量


class Graph:
    def __init__(self):
        self.N = 10   #节点node有10个
        self.L = self.N * self.N    #所有节点两两互联link
        self.D = self.N * (self.N-1)   #需求demand数
        self.graph = numpy.zeros((self.N,self.N))   #连通图为N*N矩阵
        self.f = numpy.random.random(self.D)  # f为业务需求d的流量
        self.s = numpy.random.randint(1,self.D,self.D)  #s为需求d的起始节点
        self.t = numpy.random.randint(1,self.D,self.D)  #t为需求d的目的节点
        self.edgeList = []
        self.E_r = len(self.edgeList)

    def generate_data(self):
        self.graph[0][1] = random.uniform(0.7,1)*200 + 100
        self.graph[1][0] = random.uniform(0.7,1)*200 + 100

        for i in range(1,self.N):
            self.graph[i-1][i] = random.uniform(0.7,1)*200 + 100
            self.graph[i][i-1] = random.uniform(0.7,1)*200 + 100

        for i in range(self.N):
            for j in range(self.N):
                if i==j:
                    continue
                if self.graph[i][j]>0 : #节点i和j之间已经存在边
                    self.graph[i][j] += random.uniform(0.7,1)*100 + 100
                else:
                    if random.random()>0.2 :   #以0.8的概率生成边
                        self.graph[i][j] = random.uniform(0.7,1)*200 + 100

        #print self.f
        for i in range(self.D):
            self.f[i] = random.uniform(0.3,0.4)
            self.s[i] = random.randint(0,self.N)
            tmp = random.randint(0,self.N)

            #print self.s[i]
            while True:
                if tmp==self.s[i]:
                    tmp = random.randint(0,self.N) #s和t不能为同一个节点
                else:
                    break
            self.t[i] = tmp

    def showInfo(self):
        print "拓扑图为："
        print self.graph
        print "业务需求为："
        for i in range(self.D):
            print self.s[i],'-->',self.t[i],'：',self.f[i]

    def init(self):
        self.generate_data()
        for i in range(self.N):
            for j in range(self.N):
                if self.graph[i][j]>0 :  #如果节点i和j之间存在边
                    self.edgeList.append(edge(i,j,self.graph[i][j]))

        self.E_r = len(self.edgeList)  #实际的边的数目


if __name__=='__main__':
    gra = Graph()
    gra.init()
    r = 0.001
    prob = pulp.LpProblem('linear programming',pulp.LpMinimize)
    alpha = pulp.LpVariable('alpha',0)
    x = []
    xs = 0
    for i in range(gra.D):
        for j in range(gra.N):
            for k in range(gra.N):
                xi = pulp.LpVariable("x"+str(i)+'_'+str(j)+str(k),0,1,'Binary')
                xs += r*gra.f[i]*xi
                x.append(xi)
                #prob += r*gra.f[i]*xi
    prob += alpha

    prob += alpha <= 1
    for i in range(gra.D):
        for j in range(gra.N):
            for k in range(gra.N):
                if j!=gra.s[i] and j!=gra.t[i]:
                    prob += gra.f[i]*(x[i*gra.N*gra.N+j*gra.N+k]-x[i*gra.N*gra.N+k*gra.N+j])==0
                elif j==gra.s[i]:
                    prob += gra.f[i]*(x[i*gra.N*gra.N+j*gra.N+k]-x[i*gra.N*gra.N+k*gra.N+j])==gra.f[i]
    temp = 0
    for j in range(gra.N):
        for k in range(gra.N):
            for i in range(gra.D):
                temp += gra.f[i]*x[i*gra.N*gra.N+j*gra.N+k]
            prob += temp-gra.graph[j][k]*alpha<=0
    status = prob.solve()
    # 显示结果
    print "线性规划求得的参数值为："
    n = 0
    print alpha, '=', alpha.varValue,
    for i in prob.variables():
        if n%10!=0:
            print i.name + "=" + str(i.varValue),
        else:
            print '\n'
        n += 1

    print "总共有",len(prob.variables()),"个变量"
    print '求得的问题解为',pulp.value(prob.objective)
    print status