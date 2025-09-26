#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
import mysql.connector

# 전역 변수로 데이터베이스 커넥션 및 커서 설정
mydb = None
mycursor = None
latest_gps_data = {"latitude": None, "longitude": None}

def callback(data):
    try:
        # 수신한 데이터 파싱
        parsed_data = data.data.split(',')
        
        if len(parsed_data) < 1:
            rospy.logwarn("Received data is not in the expected format.")
            return
        
        car = parsed_data[0]
        
        # 최신 GPS 데이터가 있는지 확인
        if latest_gps_data["latitude"] is None or latest_gps_data["longitude"] is None:
            rospy.logwarn("GPS data is not available yet.")
            return
        
        latitude = latest_gps_data["latitude"]
        longitude = latest_gps_data["longitude"]
        
        # 데이터 삽입 쿼리
        sql = "INSERT INTO detected_vehicle (license_plate, latitude, longitude, time) VALUES (%s, %s, %s, sysdate())"

        val = (car, latitude, longitude)

        mycursor.execute(sql, val)

        
        mydb.commit()
        rospy.loginfo("Data inserted successfully")
    except mysql.connector.Error as err:
        rospy.logerr(f"Database error: {err}")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")

def gps_callback(data):
    try:
        # GPS 데이터를 소수점 아래 15자리로 설정
        latitude = round(data.x, 15)
        longitude = round(data.y, 15)
        
        # 최신 GPS 데이터를 전역 변수에 저장
        latest_gps_data["latitude"] = latitude
        latest_gps_data["longitude"] = longitude
        
        rospy.loginfo(f"Updated latest GPS data: {latitude}, {longitude}")
    except Exception as e:
        rospy.logerr(f"Unexpected error: {e}")

def main():
    global mydb, mycursor

    rospy.init_node('ros_mysql', anonymous=True)

    # MySQL 연결
    try:
        mydb = mysql.connector.connect(
            host="192.168.176.147",
            # host="192.168.132.147",
            # host="110.11.255.113",
            user="park",
            password="qwer1234!",
            database="admindb"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as err:
        rospy.logerr(f"Failed to connect to database: {err}")
        return

    rospy.Subscriber('/carnumber', String, callback)
    rospy.Subscriber('/m_vehicle_lat_lon', Point, gps_callback)
    rospy.spin()

    mydb.close()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        if mydb:
            mydb.close()

