cmake_minimum_required(VERSION 3.17.3)

include(pico_sdk_import.cmake)

project(spi_display)
file(GLOB SOURCES "*.c")

pico_sdk_init()

add_executable(spi_display main.c ${SOURCES})

pico_enable_stdio_usb(spi_display 1)
pico_enable_stdio_uart(spi_display 0)
pico_generate_pio_header(spi_display ${CMAKE_CURRENT_LIST_DIR}/SPILCD.pio)

target_link_libraries(spi_display 
pico_stdlib
hardware_gpio
hardware_pio
hardware_interp
hardware_rtc
)

pico_add_extra_outputs(spi_display)