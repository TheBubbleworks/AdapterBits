#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/pio.h"
#include "ST7735.h"

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"
#define PICO_DEFAULT_LED_PIN 25

int main() {
    stdio_init_all();
    printf("Start!\n");

    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    printf("Blink!!\n");

    for (int i=0; i<3; i++) {
        gpio_put(LED_PIN, 1);
        sleep_ms(100);
        gpio_put(LED_PIN, 0);
        sleep_ms(100);
    }
    printf("Blinked!!\n");

    printf("PIO Add Program\n");

    PIO pio = pio0;
    uint sm = 0;
    uint offset = pio_add_program(pio, &SPILCD_program);

    printf("PIO Init\n");
    lcdPIOInit(pio, sm, offset, PIN_SDI, PIN_SCK, SERIAL_CLK_DIV);

    printf("GPIO Init\n");
    gpio_init(PIN_CS);
    gpio_init(PIN_DC);
    gpio_init(PIN_RST);

    gpio_set_dir(PIN_CS, GPIO_OUT);
    gpio_set_dir(PIN_DC, GPIO_OUT);
    gpio_set_dir(PIN_RST, GPIO_OUT);
    gpio_set_dir(PIN_BLK, GPIO_OUT);


    printf("SPI PInSet\n");

    gpio_put(PIN_CS, 0);
    gpio_put(PIN_RST, 1);
    lcdInit(pio, sm, st7735_initSeq);

    printf("LCD Start\n");

    lcdStartPx(pio, sm);

    // static char __attribute__((aligned(4))) screen_data[SCREEN_WIDTH*2 * SCREEN_HEIGHT] = { 0 };
    //printf("sizeof(screedn_data)=%d\n", sizeof(screedn_data));

    gpio_put(LED_PIN, 1);

    //clear screen
    for (int i = 0; i < SCREEN_WIDTH * SCREEN_HEIGHT; i++) {
        lcdPut(pio, sm, 0x0);  
        lcdPut(pio, sm, 0x0);
    }
        
    while (1) {
        for (int y = 0; y < SCREEN_HEIGHT ; y+=1) { 
            for (int x = 0; x < SCREEN_WIDTH ; x+=1) { 
                lcdPut(pio, sm, y);
                lcdPut(pio, sm, y);
            }                      
        }
    }
}

#pragma clang diagnostic pop