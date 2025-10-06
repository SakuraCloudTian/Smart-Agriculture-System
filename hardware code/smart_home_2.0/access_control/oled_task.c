#include <stdio.h>
#include <unistd.h>
#include "ohos_init.h"
#include "cmsis_os2.h"
#include "wifiiot_gpio.h"
#include "wifiiot_gpio_ex.h"
#include "oled_ssd1306.h"
#include "mqtt_utils.h"
#include "access_control_task.h"

//该函数对GPIO管脚及OLED进行初始化
void oledTaskInit(void)
{
    GpioInit();
    OledInit();
}

//业务函数，完成数据在OLED上显示
void oled_thread(void *arg)
{
    (void)arg;
    oledTaskInit();       //初始化
    OledFillScreen(0x00); //清屏，
    //在左上角位置显示字符串Hello, HarmonyOS
    OledShowString(0, 0, "smart home 2.0", 1);
    // printf("oled thread running ,led level:%d\r\n", fan_level);
    char line[32] = {0};

    while (1)
    {

        //组装显示湿度的字符串
        snprintf(line, sizeof(line), "The owner is %s", owner == 0 ? "out" : "in  ");
        OledShowString(0, 3, line, 1); //在（0，2）位置显示组装后的湿度字符串
        if (isCall > 0)
        {
            OledShowString(0, 5, "Doorbell ringing", 1);
        }
        else
        {
            OledShowString(0, 5, "                          ", 1);
        }
        sleep(1); //睡眠
    }
}

//创建新线程运行OledTask函数
void oled_task(void)
{
    osThreadAttr_t attr;
    attr.name = "oledThread";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = 4096;
    attr.priority = osPriorityNormal;
    if (osThreadNew(oled_thread, NULL, &attr) == NULL)
    {
        printf("[oledThread] Falied to create oledThread!\n");
    }
}
