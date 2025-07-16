import time, machine
from ds3231_port import DS3231
from machine import I2C, Pin
import dht
from bh1750 import BH1750

i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
rtc = DS3231(i2c0)

bh1750 = BH1750(0x23, i2c0)

# DHT11 센서 설정 (데이터 핀을 14번으로 설정)
sensor = dht.DHT11(Pin(14))

f = open('data.csv', 'a')
f.write("Time, Temperature, Humidity, Light\n")

print("DHT11의 온도와 습도, BH1750의 조도를 측정합니다.")

def record_data():
    while True:
        try:
            now = rtc.get_time()
            sensor.measure()  # 센서 측정 시작
            humidity = sensor.humidity()
            temperature = sensor.temperature()
            light = bh1750.measurement  # 조도 값을 측정합니다.
            
            # format: 년도, 월, 일, 시간, 분, 초 
            print("Time: {}/{}/{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
            print("Humidity: {:.2f}%".format(humidity))
            print("Temperature: {:.2f}C".format(temperature))
            print("Light: {:.2f} lux".format(light))  # 조도 값 출력
            
            # 시간, 분, 초, 온도, 습도, 조도를 파일에 저장합니다.
            f.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}, {:.2f}\n".format(
                now[0], now[1], now[2], now[3], now[4], now[5], 
                temperature, humidity, light))  # 조도 값 추가
        
        except OSError as e:
            print("센서 읽기 실패:", e)
            # 센서 오류 시 기본값으로 기록
            f.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}, {:.2f}\n".format(
                now[0], now[1], now[2], now[3], now[4], now[5], 
                -999, -999, light))
                
        # 기록 주기를 2초로 설정합니다. (DHT11은 최소 2초 간격 필요)
        time.sleep(2)

try:
    record_data()
except KeyboardInterrupt:
    pass
finally:
    print("프로그램을 종료합니다.")
    f.close()