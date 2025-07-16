from utime import sleep
from machine import Pin
import dht

# DHT11 센서 설정 (데이터 핀을 14번으로 설정)
sensor = dht.DHT11(Pin(14))

while True:
    try:
        sensor.measure()  # 센서 측정 시작
        temperature = sensor.temperature()  # 온도 측정
        humidity = sensor.humidity()  # 습도 측정
        
        print("\nTemperature: %0.2f C" % temperature)
        print("Humidity: %0.2f %%" % humidity)
    except OSError as e:
        print("센서 읽기 실패:", e)
    
    sleep(2)  # DHT11은 최소 2초 간격으로 읽어야 함