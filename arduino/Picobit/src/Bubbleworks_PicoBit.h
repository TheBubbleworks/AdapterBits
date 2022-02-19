#ifndef BUBBLEWORKS_PICOBIT_H
#define BUBBLEWORKS_PICOBIT_H

// BUILTIN_LED GPIO 25

#define P0      A0  // GPIO26
#define P1      A1  // GPIO27
#define P2      A2  // GPIO28
#define P3      7
#define P4      8
#define P5      22
#define P6      9
#define P7      10
#define P8      11
#define P9      12
#define P10      13
#define P11      17
#define P12      14
#define P13      18
#define P14      16
#define P15      19
#define P16      15
#define P19      21
#define P20      20

// Aliases
#define BTN_A   P5
#define BTN_B   P11
#define SDA     P20
#define SCL     P19
#define MOSI    P15
#define MISO    P14
#define SCK     P13

#define ALL_PINS { P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P19, P20}
#endif
