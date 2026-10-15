# Pendant firmware (stub)

The firmware is not written yet. This file fixes the hardware contract the firmware must follow: MCU pin
assignments, signal polarities, safe states and the peripherals each function uses. The behaviour it must have
(state machine, ramp, configuration menu) is specified in [../README.md](../README.md#firmware-behaviour).

Target: **STM32F072C8T6** (Cortex-M0, 48 MHz, 64 KB flash, 16 KB RAM, LQFP-48), 3.3 V. No crystal: the 48 MHz
internal RC (HSI48) runs the core and USB, trimmed by the CRS from the USB start-of-frame when USB is connected.
Suggested toolchain: STM32CubeF0 (HAL/LL) or libopencm3, or Rust (`stm32f0xx-hal`).

## Programming

- **USB-C (J5), ROM bootloader:** fit a jumper on **J7** (BOOT0 to 3V3, 2-pin 2.54 mm footprint, not fitted) and
  power the board or reset it: the chip starts its built-in USB DFU bootloader. Load with `dfu-util -a 0 -s
  0x08000000:leave -D pendant.bin` or STM32CubeProgrammer. Remove the jumper (R6 pulls BOOT0 low) to run the
  application. The firmware can also jump to the bootloader from a USB command or menu item.
- **SWD (J6, 5-pin 2.54 mm footprint, not fitted):** 1 = 3V3, 2 = SWCLK (PA14), 3 = SWDIO (PA13), 4 = NRST,
  5 = GND. Works with an ST-LINK, a Raspberry Pi Debug Probe or any CMSIS-DAP probe.

## Pin assignments

| Pin | Port | Net | Dir | Function | Active / safe state |
|---|---|---|---|---|---|
| 42 | PB6 | TM_CLK | out, open-drain | TM1637 CLK, 10 k pull-up to 5 V (R14); PB6 is 5 V tolerant | idle high |
| 43 | PB7 | TM_DIO | in/out, open-drain | TM1637 DIO (ACK is read back), 10 k pull-up to 5 V (R15) | idle high |
| 15 | PA5 | DAC_SCK | out | SPI1 SCK (AF0) to MCP4822 | |
| 17 | PA7 | DAC_SDI | out | SPI1 MOSI (AF0) to MCP4822 | |
| 14 | PA4 | DAC_CS | out | MCP4822 /CS (GPIO; LDAC is tied low, so each write latches at once) | high = idle |
| 18 | PB0 | CMD_EN | out | DG419 analog switch U15 IN. High = amplifier connected to the CMD terminal; low = CMD terminal switched to 0 V | **low** (100 k pull-down R37) |
| 19 | PB1 | EN_REQ | out | Enable request -> Q2 -> BTS4140N -> J1.3 (24 V to drive ENABLE) | **low** (100 k pull-down R26) |
| 25 | PB12 | DRV_OK_N | in | Drive OK (AKD fault relay closed) via PC817. **Low = drive OK**, high = fault or wire open | external 10 k pull-up |
| 26 | PB13 | ESTOP_N | in | E-stop contact 2. **Low = healthy (NC closed)**, high = pressed or wire open. Also holds EN off in hardware (Q3) | external 10 k pull-up, 100 nF |
| 27 | PB14 | STOP_N | in | STOP button, low = pressed. Also holds EN off in hardware (D9 BAT54) | external 10 k pull-up |
| 28 | PB15 | RUN_N | in | RUN button, low = pressed | external 10 k pull-up |
| 29 | PA8 | JOG_N | in | JOG button, low = pressed | external 10 k pull-up |
| 30 | PA9 | FWD_N | in | Selector FWD position (J4.1), low = selected | external 10 k pull-up |
| 31 | PA10 | REV_N | in | Selector REV position (J4.3), low = selected (both high = OFF; both low = wiring fault) | external 10 k pull-up |
| 10 | PA0 | ENC_A | in | Encoder emulation A (SP3485 U8 RO) -> TIM2_CH1 (AF2) | TIM2 encoder mode |
| 11 | PA1 | ENC_B | in | Encoder emulation B (SP3485 U9 RO) -> TIM2_CH2 (AF2) | |
| 39 | PB3 | LED_RUN | out | Green RUN LED D7 (1 k) | high = on |
| 40 | PB4 | LED_FLT | out | Red FAULT LED D8 (1 k) | high = on |
| 12 | PA2 | ADC_POT | ADC_IN2 | Speed knob RV1 (0..3.3 V, 1 k + 100 nF filter) | |
| 13 | PA3 | ADC_V24 | ADC_IN3 | 24 V monitor, 100 k / 10 k divider (V24 = V_ADC × 11) | |
| 32, 33 | PA11, PA12 | USB_DM_MCU, USB_DP_MCU | USB | USB full speed device (22 Ω series, USBLC6 ESD at the connector); internal D+ pull-up | |
| 34, 37 | PA13, PA14 | SWDIO, SWCLK | SWD | debug | |
| 7 | NRST | NRST | | reset, 100 nF to GND (C25), to J6.4 | |
| 44 | BOOT0 | BOOT0 | | 10 k to GND (R6); J7 to 3V3 for the ROM bootloader | low = run application |
| | PC13-15, PF0-1, PA6, PA15, PB2, PB5, PB8-11 | - | - | spare, not connected | |

## Peripherals

- **MCP4822 (U4):** SPI1, mode 0, 16 bit frames, up to 12 MHz. Word `[A/B, -, GA=1 (1×, 2.048 V), SHDN=1,
  D11..D0]`. Channel A = forward magnitude, channel B = reverse magnitude. The output stage is
  `CMD = 5.1 × (VA − VB)`, so full code on one channel is about ±10.44 V. Never drive both channels above 0 at the
  same time; clamp the code so |CMD| ≤ 10.0 V after calibration (code ≈ 3923 at 2.048 V × 5.1). One step is about
  2.55 mV at the terminal. The gain resistors are 5 %: calibrate gain and offset per direction (menu item `CAL`).
- **TM1637 (U10):** 2-wire bus, start/stop like I²C but LSB first, no address. Bit-bang PB6/PB7 as open-drain
  outputs at ≤ 100 kHz (the 10 k pull-ups to 5 V set the rise time). Common-anode display FJ5461BH: GRID1..4 =
  digits 1..4 (left to right), SEG1..8 = a..g, dp. Brightness command 0x88 | n (n = 0..7); start at 4.
- **Quadrature:** TIM2 in encoder mode 3 (count both edges of both channels, ×4), input filter about 1 µs,
  32-bit counter. Sample the counter every 100 ms for rpm.
- **ADC:** 12 bit, sample time ≥ 13.5 cycles, average 16 samples.
- **Flash config:** store the configuration in the last two 2 kB pages (0x0800F000 and 0x0800F800), one copy
  each with a CRC32 and a sequence number (write the older page), with interrupts disabled during erase/program.
- **USB:** CDC-ACM serial console for the same settings and a status read-out; enable the CRS (sync source USB
  SOF) so HSI48 stays within USB tolerance.

## Safe-state rules the firmware must keep

1. At boot, before anything else: `CMD_EN = 0`, `EN_REQ = 0`, both DAC channels written to 0, LEDs off.
2. Never set `EN_REQ = 1` unless `ESTOP_N = 0`, `DRV_OK_N = 0` and `STOP_N = 1`. The hardware also blocks it for
   STOP and E-stop, but the firmware must not rely on that.
3. Set `CMD_EN = 1` only after the drive has been enabled for ≥ 50 ms and both DAC channels are at 0; clear it
   ≥ 20 ms after the ramp reaches 0 and before or together with dropping `EN_REQ`.
4. Run the independent watchdog (IWDG, ≤ 100 ms). A watchdog reset leaves both outputs low through the pull-downs
   (all GPIOs are inputs after reset).
5. Enable the brown-out / programmable voltage detector so a sagging 3.3 V resets the MCU rather than letting it
   run out of spec.
