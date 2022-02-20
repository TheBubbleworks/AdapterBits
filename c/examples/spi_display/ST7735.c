#include "ST7735.h"

void lcdSetDC(bool dc) {
    sleep_us(1);
    gpio_put_masked((1u << PIN_DC) , !!dc << PIN_DC  );
    sleep_us(1);
}

void lcdWriteCMD(PIO pio, uint sm, const uint8_t *cmd, size_t count) {
    lcdWaitIdle(pio, sm);
    lcdSetDC(0);
    lcdPut(pio, sm, *cmd++);
    if (count >= 2) {
        lcdWaitIdle(pio, sm);
        lcdSetDC(1);
        for (size_t i = 0; i < count - 1; ++i)
            lcdPut(pio, sm, *cmd++);
    }
    lcdWaitIdle(pio, sm);
    lcdSetDC(1);
}

void lcdInit(PIO pio, uint sm, const uint8_t *init_seq) {
    const uint8_t *cmd = init_seq;
    while (*cmd) {
        lcdWriteCMD(pio, sm, cmd + 2, *cmd);
        sleep_ms( (*(cmd + 1) * 5) + 5);
        cmd += *cmd + 2;
    }
}

void lcdStartPx(PIO pio, uint sm) {
    uint8_t cmd = ST7735_RAMWR;
    lcdWriteCMD(pio, sm, &cmd, 1);
    lcdSetDC(1);
}
