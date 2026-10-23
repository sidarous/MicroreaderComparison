# Micro e-reader comparison

An interactive, to-scale comparison of thirteen pocket E Ink readers built on ESP32 microcontrollers, plus the Android-based Xteink S4 for reference.

**View it live:** https://mark.sidarous.net/MicroreaderComparison/

## What's a micro e-reader?

"Micro e-readers" are the category of pocket E Ink readers started by the Xteink X4. Instead of a phone-class Android chip, they run on a low-power ESP32-class microcontroller: mostly ESP32-C3 or ESP32-S3, though the older M5Paper v1.1 uses the original ESP32. Most of them can run [CrossPoint](https://github.com/crosspoint-reader/crosspoint-reader), an open-source reader firmware.

The **Xteink S4** is the exception. It's the same size class as the X4, but it runs Android, so it's on the page as a point of comparison. On the page, its name is marked "(Android)" and its outline is dotted.

## What the page does

- **To-scale outlines** of each device, with the screen area shaded inside the body.
- **Three layouts:** superimposed and centered, superimposed and bottom-aligned, or side by side.
- **Thickness side view:** each device seen from the side and laid flat, sorted thinnest to thickest, with its depth in mm. It uses the same scale as the Center and Bottom layouts.
- **Toggles:** turn devices on and off with the color chips or by clicking a table row. Use All / None for everything at once, and "Show screens" to hide the screen shading.
- **Hover highlighting:** hover a chip or row to bring that device to the front and dim the rest.
- **Three tables:** Size and screen, Controls and body, and Hardware. The Hardware table includes gyro and real-time clock (RTC) columns.
- **Lite models** (EEGO A4 Lite, PaperMono Lite) share their full model's color and are drawn with dashed outlines.

Everything is in one file, `index.html`, with no build step. The only outside request is the IBM Plex Sans font from Google Fonts, and the page falls back to system fonts without it.

## Devices

| Device | Chip | Screen | W × H × D (mm) | Weight | Battery | Front light | Touch | CrossPoint | Price (Oct 2026) |
|---|---|---|---|---|---|---|---|---|---|
| Xteink X4 | ESP32-C3 | 4.3" 480×800 | 69 × 114 × 5.9 | 74 g | 650 mAh | No | No | Official | $69, discontinued |
| Xteink X4 Classic | ESP32-S3 | 4.3" 480×800 | 69 × 114 × 4.9 | 68 g | 920 mAh | No | No | Official | $79 |
| Xteink X4 Pro | ESP32-S3 | 4.3" 480×800 | 69 × 111 × 5.95 | 72 g | 1100 mAh | Warm/cool | Yes | Official | $99 |
| Xteink X3 | ESP32-C3 | 3.7" 528×792 | 63.7 × 97.6 × 5.1 | 58 g | 650 mAh | No | No | Official | $69–79 |
| Boox Picco | ESP32-S3 | 3.97" 480×800 | 62 × 105.5 × 5.5 | 58 g | 920 mAh | Warm/cool | Yes | Official | $109.99 US, pre-order |
| Metalio E-Ink 4 | ESP32-S3 | 3.97" 480×800 | 63.7 × 107 × 6.8 | 70 g | 1000 mAh | No | Yes | Official | $72 |
| Seeed reTerminal Sticky | ESP32-S3 | 3.97" 480×800 | 65.5 × 106 × 7.3 | 70 g | 750 mAh | No | Yes | Official | $49.90 |
| M5Stack PaperMono | ESP32-S3 | 3.97" 480×800 | 61 × 101 × 7.95 | 74.7 g | 1150 mAh | White | Yes | Official | $65 |
| M5Stack PaperMono Lite | ESP32-S3 | 3.97" 480×800 | 61 × 101 × 8 | 72.4 g | 1150 mAh | White | Yes | Official | $55 |
| M5Stack M5Paper v1.1 | ESP32 | 4.7" 540×960 | 67 × 118.6 × 10 | 81.6 g | 1150 mAh | No | Yes | Official | $85 |
| EEGO A4 | ESP32-S3 | 3.98" 552×768 | 68.5 × 98.5 × 8 | 84 g | 2000 mAh (rated) | Warm/cool | Yes | Official | $86 |
| EEGO A4 Lite | ESP32-S3 | 3.98" 552×768 | 68.5 × 98.5 × 8 | 78 g | 2000 mAh (rated) | No | Yes | Official | $66 |
| LilyGo T5 E-Paper S3 Pro Lite | ESP32-S3 | 4.7" 540×960 | 69 × 129 × 11 | 100+ g | 1500 mAh | White | Yes | Community forks | $71.31 |
| Xteink S4 (Android) | Rockchip RK3326 | 4.3" 480×800 | 70 × 112 × 6.98 | 95 g | 1400 mAh | Warm/cool | Yes | No (KOReader preinstalled) | RMB 339–499, China only |

The page also covers RAM, gyro, RTC, charging port, button counts, and magnetic backs. The thinnest device is the X4 Classic at 4.9 mm, and the thickest is the LilyGo at 11 mm.

A few notes on availability:

- **Xteink X3:** some AliExpress units ship with USB flashing locked.
- **Boox Picco:** $99.99 in Hong Kong, shipping late October to November.
- **EEGO A4 and A4 Lite:** Chinese-only stock firmware, with publicly reported quality-control issues. Earlier China listings were about RMB 239 (~$35).
- **M5Stack PaperMono and PaperMono Lite:** the Lite drops the PaperMono's LoRa and NFC. Both are sold in limited batches; M5Stack says the next batch comes next year.
- **LilyGo T5 S3 Pro Lite:** a developer board, not a finished reader.
- **Xteink S4:** went on pre-sale in China on September 14, 2026, at RMB 339 (about $48) for the first batch, then RMB 499 (about $70). Xteink has announced no international release, so it has to be imported.

## Data caveats

- **Screen sizes are calculated, not measured.** Each screen's width and height come from its diagonal and resolution. Screens are drawn centered in the body, so bezels are approximate (Xteink devices actually have a larger bottom chin). The exception is the PaperMono Lite, whose screen size (50.84 × 86.4 mm) and position come from M5Stack's drawing.
- **Screen-to-body ratio** uses the front footprint only.
- **Original X4 RAM** is about 400 KB. Xteink's early "128 MB" claim was wrong.
- **Button counts** are physical keys, and a rocker counts as two, so the Boox Picco's rocker, function switch, and power key add up to 4. The X4 Classic and X3 counts are inferred from a review, not from a key-by-key spec. The PaperMono count (shown as "5?") is unconfirmed. The LilyGo's user key is treated as the Home button CrossPoint lists.
- **LilyGo dimensions** come from the T5 S3 Pro wiki. LilyGo says the Lite shares the Pro's design, minus LoRa and GPS. Its weight and white front light come from CrossPoint's device list.
- **Gyro and RTC** follow CrossPoint's device list. The original X4 has neither, the Metalio has an RTC but no gyro, and the S4 has both.
- **Lite models:** the EEGO A4 Lite is drawn with the A4's body. The PaperMono Lite uses M5Stack's drawing (61 × 101 × 8 mm, with an 8.7 mm bottom chin). In CrossPoint's list, the EEGO A4 Lite differs from the A4 only in weight and front light, and the PaperMono Lite is lighter than the PaperMono and has no LoRa or NFC.
- **EEGO A4 screen** is 3.98", per CrossPoint's device list.
- **M5Paper v1.1** dimensions come from M5Stack's drawing (67 × 118.6 × 10 mm). Its weight is CrossPoint's 81.6 g; M5Stack's spec sheet says 86 g.
- **EEGO battery** is the maker's rated figure and hasn't been independently verified.
- **"Not listed" for magnets** means the maker doesn't mention one, not a confirmed "no".
- **Xteink S4:**
  - It runs a 32-bit Android 11 Go build on a quad-core Rockchip RK3326, so 64-bit-only apps won't install.
  - Its security patch is from October 2021, which is hard to defend on a 2026 device.
  - KOReader comes preinstalled as a system app and is the main ePub reader.
  - Some spec sheets list its resolution as 800 × 600 rather than 480 × 800.
  - The 112 × 70 mm footprint comes from a single pre-launch report. Thickness (6.98 mm) and weight (95 g) are the most widely reported figures, though one source gives 89 g.
  - Reports disagree on the buttons: physical side page-turn keys plus a front Home key that may be capacitive.

## Devices left out

- **Murphy M4:** width, height, and weight are unpublished, so it can't be drawn to scale.
- **Metalio E-Ink 4 Plus:** 4.7", 684×1216, 122 × 71 × 7.8 mm. Weight and price unconfirmed.
- **EEGO P4:** Android-based, so outside the ESP32 category. (The Android Xteink S4 is included, but only for reference.)
- **Xteink X4 Light:** leaked only, with no confirmed specs.
- **M5Stack PaperS3:** end of life.

## Editing the data

All device data is in the `devs` array near the top of the `<script>` in `index.html`. Each entry has:

| Field | Meaning |
|---|---|
| `n`, `s` | Full name and short chip label |
| `c`, `d` | Outline color (hex) and optional SVG dash pattern |
| `on` | Whether the device is shown when the page loads |
| `w`, `h`, `t` | Body width, height, and depth in mm |
| `sw`, `sh` | Screen width and height in mm |
| `sy` | Optional: screen's distance from the top of the body in mm. Without it, the screen is centered. |
| `diag`, `res`, `ppi`, `g` | Diagonal, resolution, PPI, and weight (as display strings) |
| `chip`, `ram`, `bat`, `chg`, `btn` | Chip, RAM, battery (mAh, a number), charging, and buttons |
| `fl`, `tch`, `mag`, `cp`, `gy`, `rtc` | Front light, touch, magnet, CrossPoint, gyro, and RTC tags |

Tag fields are `[class, label]` pairs. The class sets the color: `y` is green, `n` is gray, and `p` is amber.

To get the screen size from a diagonal of `D` inches and a resolution of `a × b`:

```
sw = D × 25.4 × a / √(a² + b²)
sh = D × 25.4 × b / √(a² + b²)
```

## Ideas

- Sort a table by clicking a column header (for example by weight or battery).
- Add the Metalio E-Ink 4 Plus.
- Fill the gaps: Metalio RAM and port type, and the PaperMono button count.

## Sources

- [TechRadar: Xteink model comparison](https://www.techradar.com/tablets/ereaders/which-mini-xteink-ereader-should-you-buy-ive-crunched-the-numbers-on-all-4-models-heres-my-verdict-as-an-x4-pro-owner)
- [Product Impossible: pocket e-readers roundup](https://productimpossible.com/articles/pocket-e-readers-2026/)
- [GBAtemp: Xteink X4 hardware review](https://gbatemp.net/review/xteink-x4.2718/)
- [Tablet Sage: Xteink X4 Pro review](https://tabletsage.com/xteink-x4-pro-review/)
- [Xteink: X4 Pro FAQ and specs](https://www.xteink.com/blogs/product/x4-pro-faq-specs-support)
- [CrossPoint Reader on GitHub](https://github.com/crosspoint-reader/crosspoint-reader)
- [Boox: Picco store page](https://shop.boox.com/products/picco)
- [PocketInk: Boox Picco vs Xteink](https://pocketink.io/blog/boox-picco-vs-xteink/)
- [Joshua Lowcock: EEGO A4 review](https://www.joshualowcock.com/eego/first-review-eego-a4-microreader/)
- [Metalio E-Ink 4 hardware repo](https://github.com/CloudZao/Metalio-E-INK4)
- [CrossPoint Reader: Devices](https://crosspointreader.com/devices)
- [Seeed: reTerminal Sticky](https://www.seeedstudio.com/sticky/)
- [M5Stack: PaperMono store page](https://shop.m5stack.com/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display)
- [CNX Software: M5Stack PaperMono](https://www.cnx-software.com/2026/08/21/m5stack-paper-mono-an-esp32-s3-e-paper-development-board-with-3-97-inch-touchscreen-lora-and-nfc/)
- [M5Stack: M5Paper v1.1 docs](https://docs.m5stack.com/en/core/Paper_v1.1)
- [LilyGo: T5 S3 Pro wiki](https://wiki.lilygo.cc/products/t5-series/t5-e-paper-s3-pro/)
- [LilyGo: T5 S3 Pro Lite store page](https://lilygo.cc/en-us/products/t5-e-paper-s3-pro-lite)
- [Read with Pro: Murphy M4 specs](https://www.readwithpro.com/devices/murphy-m4)
- [Notebookcheck: Xteink S4 debuts with Android 11](https://www.notebookcheck.net/Xteink-S4-Pocket-e-reader-debuts-with-Android-11-4-3-inch-display-and-32GB.1400952.0.html)
- [Good e-Reader: Xteink S4 is available now](https://goodereader.com/blog/electronic-readers/xteink-s4-is-available-now-with-usb-c-and-a-front-light)
- [The eBook Reader: Xteink S4 released](https://blog.the-ebook-reader.com/2026/09/15/xteink-s4-released-with-android-frontlight-and-usb-c/)
- [PocketInk: Xteink S4 China release, price, and specs](https://pocketink.io/blog/xteink-s4-everything-we-know/)
- [Joshua Lowcock: Xteink S4 guide](https://www.joshualowcock.com/xteink/guide-xteink-s4-all-we-know-about-the-potential-successor-to-the-x4/)
