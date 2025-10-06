#include <stdio.h>
#include <unistd.h>
#include "ohos_init.h"
#include "cmsis_os2.h"
#include "wifiiot_gpio.h"
#include "wifiiot_gpio_ex.h"
#include "oled_ssd1306.h"
#include "temp_and_hum_task.h"
// #include "soil_moisture_task.h"
#include "toilet_task.h"
#include "mqtt_task.h"
#include "fan_task.h"   
//该函数对GPIO管脚及OLED进行初始化
void oledTaskInit(void)
{
    GpioInit();
    OledInit();
}

//业务函数，完成数据在OLED上显示
void oledThread(void *arg)
{
    (void)arg;
    oledTaskInit();       //初始化
    OledFillScreen(0x00); //清屏，
    //在左上角位置显示字符串Hello, HarmonyOS
    OledShowString(0, 0, "smart shed 2.0", 1);
    char line[32] = {0};

    while (1)
    {

        //组装显示温度字符串
        snprintf(line, sizeof(line), "temp: %3d", temp);
        OledShowString(0, 1, line, 1); //在（0，2）位置显示组装后的温度字符串
        snprintf(line, sizeof(line), "hum : %3d", hum);
        OledShowString(0, 2, line, 1); //在（0，2）位置显示组装后的湿度字符串
        snprintf(line, sizeof(line), "light_state:%3d", toilet_light_state);
        OledShowString(0, 3, line, 1); //在（0，2）位置显示led灯状态字符串
        snprintf(line, sizeof(line), "intensity:%3d", intensity);
        OledShowString(0, 4, line, 1); //在（0，2）位置显示光照强度字符串
        snprintf(line, sizeof(line), "fan_level : %3d", fan_level);
        OledShowString(0, 5, line, 1); //在（0，2）位置显示组装后的风扇等级字符串
        snprintf(line, sizeof(line), "temp_set : %3d", temp_set);
        OledShowString(0, 6, line, 1); //在（0，2）位置显示设定的温度
        sleep(1);                      //睡眠
    }
}

//创建新线程运行OledTask函数
void oledTask(void)
{
    osThreadAttr_t attr;
    attr.name = "oledThread";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = 4096;
    attr.priority = osPriorityNormal;
    if (osThreadNew(oledThread, NULL, &attr) == NULL)
    {
        printf("[oledThread] Falied to create oledThread!\n");
    }
}
