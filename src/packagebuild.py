import os
import json
import blog
import re

class package_build():
    
    #
    # Returns a package_build object
    # from a given json_str
    #
    @staticmethod
    def from_json(json_str):
        json_obj = json.loads(json_str)
        return package_build.from_dict(json_obj)
    
    @staticmethod
    def from_dict(pkgbuild_dict):
        package_build_obj = package_build()

        package_build_obj.name = package_build.try_get_json_value(pkgbuild_dict, "name")
        package_build_obj.real_version = package_build.try_get_json_value(pkgbuild_dict, "real_version")
        package_build_obj.version = package_build.try_get_json_value(pkgbuild_dict, "version")
        package_build_obj.source = package_build.try_get_json_value(pkgbuild_dict, "source")
        
        package_build_obj.extra_sources = package_build.try_get_json_value(pkgbuild_dict, "extra_sources")
        package_build_obj.description = package_build.try_get_json_value(pkgbuild_dict, "description")
        package_build_obj.dependencies = package_build.try_get_json_value(pkgbuild_dict, "dependencies")
        package_build_obj.build_dependencies = package_build.try_get_json_value(pkgbuild_dict, "build_dependencies")
        package_build_obj.cross_dependencies = package_build.try_get_json_value(pkgbuild_dict, "cross_dependencies")

        package_build_obj.build_script = package_build.try_get_json_value(pkgbuild_dict, "build_script")
        return package_build_obj

    #
    # Returns a package_build object
    # from a given file
    #
    @staticmethod
    def from_file(file_path):
        # Check for file
        if(not os.path.exists(file_path)):
            blog.error("Could not load packagefile.")
            return -1
        
        with open(file_path, "r") as build_file:
            return package_build.from_string(build_file.read())

    #
    # Returns a package_build object
    # from a given pkgbuild as a string
    #
    @staticmethod
    def from_string(pkgbuild_str):
        pkg_build_arr = pkgbuild_str.split("\n")
        package_build_obj = package_build()

        build_opts = False
        command = ""
        for prop in pkg_build_arr:

            #
            # build_opts mode (Build script)
            #
            if(build_opts):
                if(prop == "}"):
                    build_opts = False
                    continue
                
                package_build_obj.build_script.append(prop)
            
            #
            # Regular option parsing mode
            #
            else:
                divider = prop.find("=")
                key = prop[0:divider]
                val = prop[divider+1:len(prop)]

                if(val is None):
                    continue
                
                match key:
                    case "name":
                        if(val is None):
                            package_build_obj.name = None
                        else:
                            package_build_obj.name = "{}".format(val)
                    
                    case "version":
                        if(val is None):
                            package_build_obj.version = None    
                        else:
                            package_build_obj.version = "{}".format(val)

                    case "real_version":
                        package_build_obj.real_version = val
                    
                    case "source":
                        package_build_obj.source = "{}".format(val)
                
                    case "extra_sources":
                        package_build_obj.extra_sources = package_build.parse_str_to_array(val) 

                    case "dependencies":
                        package_build_obj.dependencies = package_build.parse_str_to_array(val)
   
                    case "description":
                        package_build_obj.description = "{}".format(val)
                        
                    case "builddeps":
                        package_build_obj.build_dependencies = package_build.parse_str_to_array(val)
                    
                    case "crossdeps":
                        package_build_obj.cross_dependencies = package_build.parse_str_to_array(val)
                    
                    case "build":
                        build_opts = True
        
        blog.debug("Parsed packagebuild object is: {}".format(package_build_obj.__dict__))
        return package_build_obj
   
    #
    # Returns a package_build object
    # from a given pkgbuild as provided by SQLite
    #
    @staticmethod
    def from_list(plist):
        package_build_obj = package_build()
        package_build_obj.name = plist[0]
        package_build_obj.real_version = plist[1]
        package_build_obj.version = plist[2]
        package_build_obj.source = plist[3]
        package_build_obj.extra_sources = package_build.parse_str_to_array(plist[4])
        package_build_obj.description = plist[5]
        package_build_obj.dependencies = package_build.parse_str_to_array(plist[6])
        package_build_obj.build_dependencies = package_build.parse_str_to_array(plist[7])
        package_build_obj.cross_dependencies = package_build.parse_str_to_array(plist[8])
        package_build_obj.build_script = plist[9].split("\n")
        
        blog.debug("Parsed packagebuild object is: {}".format(package_build_obj.__dict__))
        return package_build_obj
    #
    # Attempts to fetch a value by a given key,
    # returns None on KeyError
    #
    @staticmethod
    def try_get_json_value(json_obj, key):
        try:
            return json_obj[key]
        except KeyError:
            blog.debug("Key={}: No such key found. key=None".format(key)) 
            return None

    #
    # Parses branchpackagebuild array format:
    # [a][b][c]
    #
    @staticmethod
    def parse_str_to_array(string):
        vals = [ ]
        buff = ""

        for c in string:
            if(c == ']'):
                vals.append(buff)
                buff = ""
            elif(not c == '['):
                buff = buff + c

        return vals

    #
    # Empty object
    #
    def __init__(self):
        self.name = None
        self.version = None
        self.real_version = None
        self.dependencies = [ ]
        self.build_dependencies = [ ]
        self.cross_dependencies = [ ]
        self.source = None
        self.extra_sources = [ ]
        self.description = None
        self.build_script = [ ]

    #
    # Get self as dict
    #
    def get_dict(self):
        res = { }
        res["name"] = self.name
        res["version"] = self.version
        res["real_version"] = self.real_version
        res["dependencies"] = self.dependencies
        res["build_dependencies"] = self.build_dependencies
        res["cross_dependencies"] = self.cross_dependencies
        res["source"] = "{}".format(self.source)
        res["extra_sources"] = self.extra_sources
        res["description"] = self.description
        res["build_script"] = self.build_script
        return res

    #
    # Get self as json
    #
    def get_json(self):
        return json.dumps(self.get_dict())
    
    #
    # Get self as string
    #
    def get_string(self):
        res = ""
        
        res += ("name={}\n".format(self.name))
        res += ("version={}\n".format(self.version))
        res += ("description={}\n".format(self.description))
        res += ("real_version={}\n".format(self.real_version))
        res += ("source={}\n".format(self.source))

        # write extra_sources array in bpb format
        res += ("extra_sources=")
        
        for exs in self.extra_sources:
            res += ("[{}]".format(exs))

        res += ("\n")
        res += ("dependencies=")
        
        if(not self.build_dependencies is None):
            for dep in self.dependencies:
                res += ("[{}]".format(dep))
    
        res += ("\n")
        res += ("builddeps=")
        

        if(not self.build_dependencies is None):
            for dep in self.build_dependencies:
                res += ("[{}]".format(dep))

        res += ("\n")
        res += ("crossdeps=")
        
        if(not self.cross_dependencies is None):
            for dep in self.cross_dependencies:
                res += ("[{}]".format(dep))
       
        res += ("\n")
        res += ("build={\n")
        
        for line in self.build_script:
            res += (line)
            res += ("\n")

        res += ("}")
        return res 



    #
    # write build file to disk
    #
    def write_build_file(self, file):
        with open(file, "w") as package_build_file:
            package_build_file.write("name={}\n".format(self.name))
            package_build_file.write("version={}\n".format(self.version))
            package_build_file.write("description={}\n".format(self.description))
            package_build_file.write("real_version={}\n".format(self.real_version))
            package_build_file.write("source={}\n".format(self.source))

            # write extra_sources array in bpb format
            package_build_file.write("extra_sources=")
            
            for exs in self.extra_sources:
                package_build_file.write("[{}]".format(exs))

            package_build_file.write("\n")
            package_build_file.write("dependencies=")
            
            if(not self.build_dependencies is None):
                for dep in self.dependencies:
                    package_build_file.write("[{}]".format(dep))
        
            package_build_file.write("\n")
            package_build_file.write("builddeps=")
            

            if(not self.build_dependencies is None):
                for dep in self.build_dependencies:
                    package_build_file.write("[{}]".format(dep))

            package_build_file.write("\n")
            package_build_file.write("crossdeps=")
            
            if(not self.cross_dependencies is None):
                for dep in self.cross_dependencies:
                    package_build_file.write("[{}]".format(dep))
           
            package_build_file.write("\n")
            package_build_file.write("build={\n")
            
            for line in self.build_script:
                package_build_file.write(line)
                package_build_file.write("\n")

            package_build_file.write("}")
    
    #
    # Checks if a package build is valid
    #
    def is_valid(self):
        # check if name is None
        if(self.name == None or self.version == None or self.real_version == None):
            return False

        # check if required fields are set
        if(self.name == "" or self.version == "" or self.real_version == ""):
            return False

        # check if real_version is number
        if(not self.real_version.isdigit()):
            return False

        # only -, _, numbers and letters are allowed as the pkgname
        regex = re.compile('[a-zA-Z0-9_+-]+')
        if(not regex.fullmatch(self.name)):
            return False
    
        # check if build tag is valid
        encountered_closing_tag = False
        closing_tag_error = False

        for line in self.build_script:
            # if we continue iterating after we have seen a closing tag, the pkgbuild is invalid.
            if(encountered_closing_tag):
                closing_tag_error = True
                break
             
            # set this to true if we see a closing tag
            if(line == "}"):
                encountered_closing_tag = True

        # build invalid, because closing tag error
        if(closing_tag_error):
            return False

        return True
