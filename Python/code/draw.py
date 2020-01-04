def draw(data,center):
    length=len(center)
    fig=plt.figure
    # 绘制原始数据的散点图
    plt.scatter(data[:,0],data[:,1],s=25,alpha=0.4)
    # 绘制簇的质心点
    for i in range(length):
        plt.annotate('center',xy=(center[i,0],center[i,1]),xytext=\
        (center[i,0]+1,center[i,1]+1),arrowprops=dict(facecolor='red'))
    plt.show()
