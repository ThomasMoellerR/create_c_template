import argparse
import time
import os
import time
import shutil


nl = "\n" # newline
ss = "\"" # string sign


def open_sector():
	a = "/"
	for i in range(78):
		a += "*"
	a += nl
	return a

def close_sector():
	a = ""
	for i in range(78):
		a += "*"
	a += "/"
	a += nl
	return a

def abstand():
	a = ""
	a += "*" 
	for i in range(2):
		a += " "
	return a

def write_text(text):
	a = ""
	a += abstand()
	a += "{:15s}:  ".format(text)
	return a

def insert_sector_name(sector_name):
	a = ""
	a += abstand()
	a += sector_name
	a += nl
	return a

def create_sector(sector_name):
	a = ""
	a += nl
	a += open_sector()
	a += insert_sector_name(sector_name)
	a += close_sector()
	return a

def create_header(name, typ, version): # Kopf
	t = time.strftime("%Y-%m-%d %H:%M:%S")
	a = ""
	a += nl
	a += open_sector()
	a += write_text("File") + name + typ + nl
	a += write_text("Version") + version + nl
	a += write_text("Last Changes") + t + nl
	a += close_sector()
	return a

def create_define_start(name):
	a = ""
	a += nl
	a += "#ifndef __"
	a += name.upper()
	a += "_H"
	a += nl
	a += "#define __"
	a += name.upper()
	a += "_H"
	a += nl
	
	return a

def create_define_end(name):
	a = ""
	a += "#endif /* __"
	a += name.upper()
	a += "_H */"
	a += nl
	return a

def create_ini_prototyp(name):
	a = ""
	a += nl
	a += "extern void "
	a += name.upper()
	a += "_Ini (void);"
	a += nl
	return a

def create_ini_function(name):
	a = ""
	a += nl
	a += "void "
	a += name.upper()
	a += "_Ini (void)" + nl
	a += "{" + nl
	a += nl
	a += "}" + nl
	return a

def create_changes_section():
	a = ""
	a += nl
	a += open_sector()
	a += write_text("Changes") + nl
	a += abstand() + "{:16s}  ".format("") + nl
	a += abstand() + "{:16s}  ".format("") + nl
	a += abstand() + "{:16s}  ".format("") + nl
	a += close_sector()
	return a


def create_function_description():
	a = ""
	a += nl
	a += open_sector()
	a += write_text("Function Name") + nl
	a += write_text("Description") + nl
	a += write_text("Parameter(s)") + nl
	a += write_text("Return Value") + nl
	a += close_sector()
	return a

def end_of_file(name):
	a = ""
	a += nl
	a += open_sector()
	a += write_text("END OF FILE") + name + ".h" + nl
	a += close_sector()
	return a	

def create_extern_c_start():
	a = ""
	a += nl
	a += "#ifdef __cplusplus"
	a += nl
	a += "extern \"C\" {"
	a += nl
	a += "#endif"
	a += nl
	return a

def create_extern_c_end():
	a = ""
	a += nl
	a += "#ifdef __cplusplus" + nl
	a += "}" + nl
	a += "#endif" +nl
	a += nl
	return a

def include_own_file():
	a = ""
	#a += nl
	a += "#include \"" + args.modul_name + ".h\"" + nl
	return a
	
def include_typ_h():
	a = ""
	a += nl
	a += "#include \"typ.h\"" + nl
	return a

def create_extern_variable_declaration(name):
	a = ""
	a += nl
	a += "extern TUINT8 "
	a += name.upper()
	a += "_Temp;"
	a += nl
	return a

def create_extern_variable_definition(name):
	a = ""
	a += nl
	a += "TUINT8 "
	a += name.upper()
	a += "_Temp = 0;"
	a += nl
	return a


# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--output_folder", help="")
parser.add_argument("--modul_name", help="")
args = parser.parse_args()

# Deletes output Folder and creates output folder. All files will be deleted.
try: shutil.rmtree(args.output_folder)
except: pass
os.makedirs(args.output_folder, exist_ok=True)


# Create .c File
a = ""
a += create_header(args.modul_name, ".c","1")
a += create_sector("Include Files")
a += include_typ_h()
a += include_own_file()
a += create_sector("Local Constants")
a += create_sector("Local Type Definitions")
a += create_sector("Local Variables")
a += create_sector("Global Variables")
a += create_extern_variable_definition(args.modul_name)
a += create_sector("Local Function Prototypes")
a += create_sector("Local Functions")
a += create_sector("Global Functions")
a += create_function_description()
a += create_ini_function(args.modul_name)
a += create_changes_section()
a += end_of_file(args.modul_name)

f = open(os.path.join(args.output_folder,args.modul_name + ".c"), "w")
f.write(a)
f.close()

#print(a)



# Create .h File
a = ""
a += create_header(args.modul_name, ".h","1")
a += create_define_start(args.modul_name)
a += create_extern_c_start()
a += create_sector("Include Files")
a += include_typ_h()
a += create_sector("Global Constants")
a += create_sector("Global Type Definitions")
a += create_sector("Global Variables")
a += create_extern_variable_declaration(args.modul_name)
a += create_sector("Global Function Prototypes")
a += create_ini_prototyp(args.modul_name)
a += create_changes_section()
a += create_extern_c_end()
a += create_define_end(args.modul_name)
a += end_of_file(args.modul_name)

f = open(os.path.join(args.output_folder,args.modul_name + ".h"), "w")
f.write(a)
f.close()

#print(a)







