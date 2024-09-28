
GET_POWER_STATE = [0x10, 0xFF, 0x04, 0x0F]
SET_POWER_ON = [0x10, 0xFF, 0x04, 0x1F, 0x01]
SET_POWER_OFF = [0x10, 0xFF, 0x04, 0x1F, 0x00]
GET_BRIGHTNESS_INFO = [0x10, 0xFF, 0x04, 0x2F, 0x00]
GET_BRIGHTNESS = [0x10, 0xFF, 0x04, 0x3F]
SET_BRIGHTNESS = [0x10, 0xFF, 0x04, 0x4F, 0x00, 0x00]
GET_BRIGHTNESS_LEVELS = [0x10, 0xFF, 0x04, 0x5F]
GET_COLOR_TEMPERATURE_INFO = [0x10, 0xFF, 0x04, 0x7F, 0x00, 0x00, 0x00]
GET_COLOR_TEMPERATURE = [0x10, 0xFF, 0x04, 0x8F]
SET_COLOR_TEMPERATURE = [0x10, 0xFF, 0x04, 0x9F, 0x00, 0x00]
GET_COLOR_TEMPERATURE_LEVELS = [0x10, 0xFF, 0x04, 0xAF]



"""
GetBrightness() -> 40
3643.607 t:1683292550 W: 10 FF 04 3F 
3643.608 t:1683292550 R: 11 FF 04 3F 00 28 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

SetBrightness(50)
3755.571 t:1683292662 W: 10 FF 04 4F 00 32 
3755.572 t:1683292662 R: 11 FF 04 4F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

GetBrightnessLevels() -> { type: non-linear, values: { 52, 96, 140, 240, 400 } }
3845.638 t:1683292752 W: 10 FF 04 5F 00 
3845.639 t:1683292752 R: 11 FF 04 5F A0 05 00 34 00 60 00 8C 00 F0 01 90 00 00 00 00 

GetColorTemperature() -> 3300
3707.616 t:1683292614 W: 10 FF 04 8F 
3707.617 t:1683292614 R: 11 FF 04 8F 0C E4 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

SetColorTemperature(4300)
3810.269 t:1683292717 W: 10 FF 04 9F 10 CC 
3810.270 t:1683292717 R: 11 FF 04 9F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

GetColorTemperatureLevels() -> { type: non-linear, values: { 2700, 3400, 4500, 5000, 6500 } }
3889.402 t:1683292796 W: 10 FF 04 AF 00 
3889.403 t:1683292796 R: 11 FF 04 AF A0 05 0A 8C 0D 48 11 94 13 88 19 64 00 00 00 00 

GetBrightnessInfo() -> { min: 30, max: 400, res: 1, maxLevels: 7,
  hasEvents: yes, hasLinearLevels: no, hasNonLinearLevels: yes, hasDynamicMaximum: yes }
GetColorTemperatureInfo() -> { min: 2700, max: 6500, res: 100, maxLevels: 7,
  hasEvents: yes, hasLinearLevels: no, hasNonLinearLevels: yes, hasDynamicMaximum: no }
  """
