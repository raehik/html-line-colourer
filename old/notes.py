os_name = sys.platform
if os_name == "win32":
    print("Running on Windows")
else:
    print("Error: os_name not win32 (" + os_name + ")")
    

while i < len(the_list):
    do_stuff(the_list[i:i+2])
    i += 3