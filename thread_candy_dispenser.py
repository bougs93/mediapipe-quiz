'''
캔디 지급기

'''

from setup import *
import re, datetime, time, sys, os
from PySide6.QtCore import QTime
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo



# class ThreadQRScanner(QThread):
class CandyDispenser(QObject):
    CandyDispensor_signal = Signal(str)

    def __init__(self):
        super().__init__()

        self.candy_dispensor_port = CANDY_DISPENSER_PORT
        self.candy_dispensor_speed = CANDY_DISPENSER_SPEED 

        self.ignore_flag = False  # 데이터를 무시할지 여부를 결정하는 플래그

    def stop(self):
        self.quit()
        self.wait(5000)

    # def run(self):
    def open(self):

        print('**************************************')
        print('** Candy dispensor 시리얼 포트 Check **')
        print('**************************************')

        # serial port 초기화
        self.serial_init()

        # 시그널 슬롯 연결 (QtCore.QIODevice)
        # 시리얼 포트로 데이터를 수신 가능하게 되었을 때에 발행> readyRead 시그널
        #  https://doc.qt.io/qtforpython/PySide6/QtCore/QIODevice.html
        #  https://doc.qt.io/qtforpython/PySide6/QtCore/QIODevice.html#PySide6.QtCore.PySide6.QtCore.QIODevice.readyRead
        
        # self.port.readyRead.connect(self.read_from_port)

        self.serial_stop()


    def serial_init(self):
        # 시리얼포트 선택 : 4800, 9600, 19200, 38400, 115200
        if self.candy_dispensor_speed == 4800:
            self.baudrate = QSerialPort.Baud4800
        elif  self.candy_dispensor_speed == 9600:
            self.baudrate = QSerialPort.Baud9600
        elif  self.candy_dispensor_speed == 19200:
            self.baudrate = QSerialPort.Baud19200
        elif  self.candy_dispensor_speed == 38400:
            self.baudrate = QSerialPort.Baud38400
        elif  self.candy_dispensor_speed == 115200:
            self.baudrate = QSerialPort.Baud115200

        # 시리얼 포트 환경변수 설정
        self.port = QSerialPort()
        self.port.setBaudRate( self.baudrate )
        self.port.setPortName( self.candy_dispensor_port )
        self.port.setDataBits( QSerialPort.Data8 )
        self.port.setParity( QSerialPort.NoParity )
        self.port.setStopBits( QSerialPort.OneStop )
        self.port.setFlowControl( QSerialPort.NoFlowControl )


        # 시리얼 포트 OPEN
        ret = self.port.open(QIODevice.ReadWrite)

        # self.port.setDataTerminalReady(True)

        if ret:
            print(f" CANDY | Port {self.candy_dispensor_port} Open [OK] : {self.candy_dispensor_speed}\n")
            return True
        else:
            print(f" CANDY | Port {self.candy_dispensor_port} Open [ERR] : {self.candy_dispensor_speed}\n")
            self.serial_stop()
            return False

    def serial_stop(self):
        self.port.close()
        print(f'\n CANDY | Port {self.candy_dispensor_port} Port Close')


    def read_from_port(self):
        if self.ignore_flag:
            self.port.readAll()  # 데이터를 읽지만 처리하지 않음. 무시함.
            return
        
        ### 수신 데이터 처리
        # QThread 에서 send는 되는데, receive가 안되는 문제 
        # https://opentutorials.org/module/544/19046
        received_data = self.port.readAll()

        print(f"CANDY serial data recive : {received_data}")

        # print(f'\n SCANNER | Port data recive : {cleaned_data}')

        # # 2) 암호화 해제
        # restore_data = self.aes.decrypt(cleaned_data)
        # if restore_data == None:
        #     print(f'[복호화 ERR]')
        # else:
        #     print(f' SCANNER | restore data recive : {restore_data}')
        #     self.analysis(restore_data)


    def pause_reception(self):
        self.ignore_flag = True

    def continue_reception(self):
        self.ignore_flag = False

    ############################################################
    # WRITE | writeToPort
    ############################################################
    def serial_Write(self, data):
        ret_serial_init = self.serial_init()
        if ret_serial_init:

            # 공백을 기준으로 문자열을 나누고 바이트로 변환
            try:
                print(f"[CANDY] 데이터 전송 : {data}")
                # hex 데이터 전송
                # hex_data = QByteArray.fromHex(data.replace(' ', '').encode('utf-8'))
                
                # 문자열 데이터 전송
                # self.port.write(QByteArray(data.encode('utf-8')))
                # self.port.write(QByteArray(data))


                # 시리얼 포트로 데이터 전송
                self.port.write(data.encode())

                 #  2) 데이터 전송
                self.port.waitForBytesWritten(1000)     # 이게 있어야만, 시리얼 전송이 이루어짐

                print(f"[CANDY] 데이터 전송 : OK")

                self.serial_stop()

            except ValueError as e:
                print(f"[CANDY] Error converting HEX string: {e}")

            except AttributeError as e:
                print(f"[CANDY] Error1 serial port: {e}")
        else:
            print(f"[CANDY] Error serial port Not open ")



if __name__ == "__main__":
    app = QCoreApplication([])
    # a = ThreadQRScanner()
    # a.run()

    b= CandyDispenser()
    # b.open()

    b.serial_Write("a,100,120,140,160,n")
    sys.exit(app.exec())