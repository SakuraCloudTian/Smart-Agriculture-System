#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "ohos_init.h"
#include "cmsis_os2.h"
// #include "soil_moisture_task.h"
#include "toilet_task.h"
#include "temp_and_hum_task.h"
#include "fan_task.h"
// #include 
#include "oled_task.h"
#include "publish_task.h"

static void ss_thread(void *arg)
{
    (void)arg;
    sleep(1);
    printf("Smart Shed 2.0 Running\n");
    temp_and_hum_task();  //调用温度湿度
    toilet_task();  //调用光敏电阻模块
    fan_task();   //风扇
    oledTask();   //led显示屏
    publish_task();  //mqtt上传
}

void ss_entry(void)
{
    osThreadAttr_t attr;

    attr.name = "smart_shed_2.0";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = 4096; // 4096;
    attr.priority = osPriorityNormal;

    if (osThreadNew((osThreadFunc_t)ss_thread, NULL, &attr) == NULL)
    {
        printf("[smart_shed_2.0] Falied to create LedTask!\n");
    }
}

SYS_RUN(ss_entry);