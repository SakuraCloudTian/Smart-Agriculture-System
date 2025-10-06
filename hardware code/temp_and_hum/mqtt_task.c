#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include "ohos_init.h"
#include "cmsis_os2.h"

#include <unistd.h>
#include "hi_wifi_api.h"
//#include "wifi_sta.h"
#include "lwip/ip_addr.h"
#include "lwip/netifapi.h"

#include "lwip/sockets.h"
#include "MQTTPacket.h"
#include "transport.h"
#include "fan_task.h"
#include "temp_and_hum_task.h"
#include "toilet_task.h"
// #include "soil_moisture_task.h"

int toStop = 0;
int fan_level=0;
// int water_pump_level = 11;
int temp_G4=0;
// int temp_fan=0;
int temp_set=20;
int light_set=202;
int start_time=6;
int end_time=21;

time_t currentTime;
struct tm *localTime;
int seconds;
int hour=9;

int mqtt_connect(void)
{
	MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
	int rc = 0;
	int mysock = 0;
	unsigned char buf[200];
	int buflen = sizeof(buf);
	int msgid = 1;
	MQTTString topicString = MQTTString_initializer;
	int req_qos = 0;
	char payload[200];
	int payloadlen = strlen(payload);
	int len = 0;

	char *host = "124.222.244.117";
	int port = 1883;

	mysock = transport_open(host, port);
	if (mysock < 0)
		return mysock;

	printf("Sending to hostname %s port %d\n", host, port);

	data.clientID.cstring = "hi3861_temp_and_hum_1";
	data.keepAliveInterval = 20;
	data.cleansession = 1;
	// data.username.cstring = "testuser";
	// data.password.cstring = "testpassword";

	len = MQTTSerialize_connect(buf, buflen, &data);
	rc = transport_sendPacketBuffer(mysock, buf, len);

	/* wait for connack */
	if (MQTTPacket_read(buf, buflen, transport_getdata) == CONNACK)
	{
		unsigned char sessionPresent, connack_rc;

		if (MQTTDeserialize_connack(&sessionPresent, &connack_rc, buf, buflen) != 1 || connack_rc != 0)
		{
			printf("Unable to connect, return code %d\n", connack_rc);
			goto exit;
		}
	}
	else
		goto exit;

	/* subscribe */
	topicString.cstring = "data_control_G4";
	//数据控制主题
	// topicString.cstring = "substopic";
	len = MQTTSerialize_subscribe(buf, buflen, 0, msgid, 1, &topicString, &req_qos);
	rc = transport_sendPacketBuffer(mysock, buf, len);
	if (MQTTPacket_read(buf, buflen, transport_getdata) == SUBACK) /* wait for suback */
	{
		unsigned short submsgid;
		int subcount;
		int granted_qos;

		rc = MQTTDeserialize_suback(&submsgid, 1, &subcount, &granted_qos, buf, buflen);
		if (granted_qos != 0)
		{
			printf("granted qos != 0, %d\n", granted_qos);
			goto exit;
		}
	}
	else
		goto exit;

	//温度阈值设置主题
	/* loop getting msgs on subscribed topic */
	topicString.cstring = "data_collect_G4";
	//数据收集主题
	while (!toStop)
	{
		    // 获取当前时间
    currentTime = time(NULL);
    // 将当前时间转换为本地时间
    localTime = localtime(&currentTime);
    // hour = localTime->tm_hour; // 获取当前小时数
    // 获取秒数
    seconds = localTime->tm_sec;
	
		/* transport_getdata() has a built-in 1 second timeout,
		your mileage will vary */
		if (MQTTPacket_read(buf, buflen, transport_getdata) == PUBLISH)
		{
			unsigned char dup;
			int qos;
			unsigned char retained;
			unsigned short msgid;
			int payloadlen_in;
			unsigned char *payload_in;
			int rc;
			MQTTString receivedTopic;
			rc = MQTTDeserialize_publish(&dup, &qos, &retained, &msgid, &receivedTopic,
										 &payload_in, &payloadlen_in, buf, buflen);
			// printf("message arrived %d,%s\n", payloadlen_in, payload_in);
			// printf("\n\nmessage arrived :\r\n ---->  %s <----\n\n\n", payload_in);
			// temp_pump=water_pump_level;
			if (payloadlen_in > 0 && payloadlen_in < 30)
			{
				// printf("receive:%s \n\r",payload_in);
				// lights_controller(payload_in);
				payload_in[payloadlen_in] = '\0';
				temp_G4=atoi((char *)payload_in);
				
				if(temp_G4==200||temp_G4==201||temp_G4==202){
					light_set = temp_G4;
				printf("\n\n light_set  : ---->  %d <----\n", light_set);
				}
				//led灯控制指令接收
				if(temp_G4>=300 &&temp_G4<312){
					start_time = temp_G4-300;
				printf("\n\n light_set_start_time  : ---->  %d <----\n", start_time);
				}
				if(temp_G4>=312 &&temp_G4<324){
					end_time = temp_G4-300;
				printf("\n\n light_set_end_time  : ---->  %d <----\n", end_time);
				}
                //led灯时间控制指令接收
				if(temp_G4>=400 &&temp_G4<423){
					hour = temp_G4-400;
				printf("\n\n hour  : ---->  %d <----\n", hour);
				}
				//当前小时获取
				if(temp_G4>=0&&temp_G4<=10){
					fan_level = temp_G4;
				printf("\n\n fan_level set : ---->  %d <----\n", fan_level);
				}
				//风扇控制指令接收
				if(temp_G4>=70&&temp_G4<=170){
					temp_set=temp_G4-100;
				printf("\n\n temp set : ---->  %d <----\n", temp_set);
				if(temp>temp_set){
	            	if((temp-temp_set)<=10)
	        	    fan_level=temp-temp_set;
	        	    else
	        	    fan_level=10;
	             }
				 else
				 fan_level=0;
				}
				//温度阈值控制指令并自动控制风扇转速
				seconds=59;
				//立刻上传一次数据
			}
			rc=rc;
		}
//1min上传一次数据
 if(seconds%59==0){
	   sleep(1);
		snprintf(payload, sizeof(payload), "{\"temp\":%d,\"hum\":%d,\"fan_level\":%d,\"temp_set\":%d,\"light_state\":%d,\"intensity\":%d}", temp, hum,fan_level,temp_set,toilet_light_state,intensity);
		printf("%s\n\r", payload);
		payloadlen = strlen(payload);
		// printf("publishing reading\n");
		len = MQTTSerialize_publish(buf, buflen, 0, 0, 0, 0, topicString, (unsigned char *)payload, payloadlen);
		rc = transport_sendPacketBuffer(mysock, buf, len);
           }
		usleep(800000);
        }


	printf("disconnecting\n");
	len = MQTTSerialize_disconnect(buf, buflen);
	rc = transport_sendPacketBuffer(mysock, buf, len);
exit:
	transport_close(mysock);

	rc = rc;

	return 0;
}
