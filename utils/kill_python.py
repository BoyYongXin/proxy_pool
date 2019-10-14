import os
import codecs
def kill(pid):
    try:
        # a=os.popen('taskkill.exe /pid:' + str(pid))
        #a=os.system('taskkill.exe /pid:' + str(pid))

        a = os.system('taskkill /pid ' + str(pid)+'  -t  -f')
        if a==0:
            print('已杀死pid为%s的进程' % (pid))
        else:
            print('未杀死pid为%s的进程' % (pid))
    except OSError:
        print('没有如此进程!!!')
if __name__ == "__main__":
    data = codecs.open(r'D:\start_get_ip\pid.txt','r')
    pid=data.readlines()[-1].strip()
    kill(int(6164))