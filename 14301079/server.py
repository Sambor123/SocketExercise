import socket
import time
import threading

SERVER_ADDRESS = (HOST, PORT) = '127.0.0.1', 3333
REQUEST_QUEUE_SIZE = 5

# 字符串逆转
def reverse_string(str):
    return str[::-1]
# 处理Http请求的线程类
class Handle(threading.Thread):
    def __init__(self, clinet_socket, threadName):
        '''@summary: 初始化对象。
        
        @param clinet_socket: socket连接
        @param threadName: 线程名称。
        '''
        super(Handle, self).__init__(name = threadName)  #注意：一定要显式的调用父类的初始化函数。
        self.clinet_socket=clinet_socket
    
    def run(self):
        '''@summary: 重写父类run方法，在线程启动后执行该方法内的代码。
        '''
        request = self.clinet_socket.recv(1024)
        print('thread %s is running...' % threading.current_thread().name)
        print(request.decode())
        http_response = reverse_string(request)
        self.clinet_socket.sendall(http_response)
        time.sleep(60)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    print('thread %s is running...' % threading.current_thread().name)

    while True:
        clinet_socket, client_address = server_socket.accept()
        Handle(clinet_socket,"threading").start();

if __name__ == '__main__':
    start_server()