# Micro e-reader comparison

An interactive, to-scale comparison of ten pocket E Ink readers built on ESP32 microcontrollers.

**View it live:** https://sidarous.github.io/MicroreaderComparison/

## What's a micro e-reader?

"Micro e-readers" are the category of pocket E Ink readers started by the Xteink X4. Instead of a phone-class Android chip, they run on a low-power ESP32-C3 or ESP32-S3 microcontroller. Most of them can run [CrossPoint](https://github.com/crosspoint-reader/crosspoint-reader), an open-source reader firmware.

## What the page does

- **To-scale outlines** of each device, with the screen area shaded inside the body.
- **Three layouts:** superimposed and centered, superimposed and bottom-aligned, or side by side.
- **Toggles:** turn devices on and off with the color chips or by clicking a table row. Use All / None for everything at once, and "Show screens" to hide the screen shading.
- **Hover highlighting:** hover a chip or row to bring that device to the front.
- **Three tables:** Size and screen, Controls and body, and Hardware.

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
| M5Stack PaperMono | ESP32-S3 | 3.97" 480×800 | 61 × 101 × 7.95 | 74.7 g | 1150 mAh | Yes | Yes | Official | $65 (Lite $55) |
| EEGO A4 / A4 Pro | ESP32-S3 | 4.0" 552×768 | 68.5 × 98.5 × 8 | 76 g | 2000 mAh (rated) | A4 Pro only | Yes | Official | ~$35, China only |
| LilyGo T5 E-Paper S3 Pro Lite | ESP32-S3 | 4.7" 540×960 | 69 × 129 × 11 | Unpublished | 1500 mAh | Warm | Yes | Community forks | $71.31 |

The page also covers RAM, charging port, button layout, and magnetic backs.

A few notes on availability:

- **Xteink X3:** some AliExpress units ship with USB flashing locked.
- **Boox Picco:** $99.99 in Hong Kong, shipping late October to November.
- **EEGO A4:** Chinese-only stock firmware, with publicly reported quality-control issues.
- **M5Stack PaperMono:** sold in limited batches; M5Stack says the next batch comes next year.
- **LilyGo T5 S3 Pro Lite:** a developer board, not a finished reader.

## Data caveats

- **Screen sizes are calculated, not measured.** Each screen's width and height come from its diagonal and resolution. Screens are drawn centered in the body, so bezels are approximate (Xteink devices actually have a larger bottom chin).
- **Screen-to-body ratio** uses the front footprint only.
- **Original X4 RAM** is about 400 KB. Xteink's early "128 MB" claim was wrong.
- **X4 Classic and X3 button counts** are inferred from a review, not from a key-by-key spec.
- **LilyGo dimensions** come from the T5 S3 Pro wiki. LilyGo says the Lite shares the Pro's design, minus LoRa and GPS.
- **EEGO battery** is the maker's rated figure and hasn't been independently verified.
- **"Not listed" for magnets** means the maker doesn't mention one, not a confirmed "no".

## Devices left out

- **Murphy M4:** width, height, and weight are unpublished, so it can't be drawn to scale.
- **Metalio E-Ink 4 Plus:** 4.7", 684×1216, 122 × 71 × 7.8 mm. Weight and price unconfirmed.
- **Xteink S4 and EEGO P4:** Android-based, so outside the ESP32 category.
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
| `diag`, `res`, `ppi`, `g` | Diagonal, resolution, PPI, and weight (as display strings) |
| `chip`, `ram`, `bat`, `chg`, `btn` | Chip, RAM, battery (mAh, a number), charging, and buttons |
| `fl`, `tch`, `mag`, `cp` | Front light, touch, magnet, and CrossPoint tags |

Tag fields are `[class, label]` pairs. The class sets the color: `y` is green, `n` is gray, and `p` is amber.

To get the screen size from a diagonal of `D` inches and a resolution of `a × b`:

```
sw = D × 25.4 × a / √(a² + b²)
sh = D × 25.4 × b / √(a² + b²)
```

## Ideas

- Sort a table by clicking a column header (for example by weight or battery).
- Add a side view comparing thickness.
- Add the Metalio E-Ink 4 Plus.
- Fill the gaps: X4 Pro PSRAM size, Metalio RAM and port type, PaperMono and Metalio button counts, and LilyGo weight.

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
- [Seeed: reTerminal Sticky](https://www.seeedstudio.com/sticky/)
- [M5Stack: PaperMono store page](https://shop.m5stack.com/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display)
- [CNX Software: M5Stack PaperMono](https://www.cnx-software.com/2026/08/21/m5stack-paper-mono-an-esp32-s3-e-paper-development-board-with-3-97-inch-touchscreen-lora-and-nfc/)
- [LilyGo: T5 S3 Pro wiki](https://wiki.lilygo.cc/products/t5-series/t5-e-paper-s3-pro/)
- [LilyGo: T5 S3 Pro Lite store page](https://lilygo.cc/en-us/products/t5-e-paper-s3-pro-lite)
- [Read with Pro: Murphy M4 specs](https://www.readwithpro.com/devices/murphy-m4)
