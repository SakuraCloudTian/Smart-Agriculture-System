#include <stdio.h>
#include <unistd.h>
#include "ohos_types.h"
#include "ohos_init.h"
#include "cmsis_os2.h"
#include "wifiiot_gpio.h"
#include "wifiiot_adc.h"
#include "wifiiot_gpio_ex.h"
#include "wifiiot_errno.h"
#include "mqtt_task.h"
#define SOIL_MOISTURE_CHAN_NAME WIFI_IOT_ADC_CHANNEL_4

int intensity = 0;
int toilet_state = 0;       //卫生间工作状态
int toilet_light_state = 0; //卫生间灯的工作状态

void init(void)
{
    GpioInit();
    //设置红色,蓝 色,绿色 LED IO为输出状态
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_10, WIFI_IOT_IO_FUNC_GPIO_10_GPIO);
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_10, WIFI_IOT_GPIO_DIR_OUT);

    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_11, WIFI_IOT_IO_FUNC_GPIO_11_GPIO);
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_11, WIFI_IOT_GPIO_DIR_OUT);

    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_12, WIFI_IOT_IO_FUNC_GPIO_12_GPIO);
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_12, WIFI_IOT_GPIO_DIR_OUT);

    //光敏电阻
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_9, WIFI_IOT_IO_FUNC_GPIO_9_GPIO);
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_9, WIFI_IOT_GPIO_DIR_IN);

    // //人体红外感应
    // IoSetFunc(WIFI_IOT_IO_NAME_GPIO_7, WIFI_IOT_IO_FUNC_GPIO_7_GPIO);
    // GpioSetDir(WIFI_IOT_IO_NAME_GPIO_7, WIFI_IOT_GPIO_DIR_IN);
    // IoSetPull(WIFI_IOT_IO_NAME_GPIO_7, WIFI_IOT_IO_PULL_UP);
}

void toilet_entry(void *arg)
{
    (void)arg;
  unsigned short data = 0;
    init();
    WifiIotGpioValue rel = 0;
    while (1)
    {

        // //读取人体红外传感器，
        // GpioGetInputVal(WIFI_IOT_IO_NAME_GPIO_7, &rel);

        // toilet_state = rel;
        //读取光敏电阻
        GpioGetInputVal(WIFI_IOT_IO_NAME_GPIO_9, &rel);
        if(light_set==200){
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_10,0);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_11,0);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_12,0);
            toilet_light_state =0;
        }
        if(light_set==201){
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_10,1);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_11,1);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_12,1);
            toilet_light_state =1;
        }
        if(light_set==202){
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_10, (int)rel);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_11, (int)rel);
            GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_12, (int)rel);
            toilet_light_state = rel;

            if(hour>end_time||hour<start_time){
               GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_10,0);
               GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_11,0);
               GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_12,0);
            toilet_light_state =0;
            }
            
            //超过规定时间 自动模式强制关闭灯光
        }
        //控制led灯的三种指令
        if (AdcRead(SOIL_MOISTURE_CHAN_NAME, &data, WIFI_IOT_ADC_EQU_MODEL_4, WIFI_IOT_ADC_CUR_BAIS_DEFAULT, 0) == WIFI_IOT_SUCCESS)
        {
            intensity = 2000 - data;
        }
        // else
        // {
        //     GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_10, WIFI_IOT_GPIO_VALUE0);
        //     GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_11, WIFI_IOT_GPIO_VALUE0);
        //     GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_12, WIFI_IOT_GPIO_VALUE0);
        //     toilet_light_state = 0;
        // }

        sleep(1);
    }
}

void toilet_task(void)
{

    osThreadAttr_t attr;
    attr.name = "toilet_task";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = 4096;
    attr.priority = osPriorityNormal;

    if (osThreadNew(toilet_entry, NULL, &attr) == NULL)
    {
        printf("[toilet_entry] Falied to create toilet_entry!\n");
    }
}
