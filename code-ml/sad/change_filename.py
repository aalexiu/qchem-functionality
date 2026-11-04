import sys

def replace_new_filename(file,new_filename):
    
    f_script = open(file,"r")

    f_out = open("submit.sh","w+")

    for line in f_script:
        if "fname" in line:
            f_out.write(line.replace("fname",new_filename))
        else: f_out.write(line)

    f_script.close()
    f_out.close()

try:
    if sys.argv.__len__() > 1:
        new_filename = sys.argv[1]
except:
    print("new filename not added")

replace_new_filename("submit_template.sh",new_filename)

