import packagebuild
import leafpkg
import os

SAMPLE_JSON = "{\"name\": \"doas\", \"version\": \"6.8.2\", \"real_version\": \"0\", \"dependencies\": [\"linux-pam\"], \"build_dependencies\": [\"linux-pam\", \"bash\", \"autoconf\", \"shadow\"], \"cross_dependencies\": [], \"source\": \"https://github.com/Duncaen/OpenDoas/releases/download/v6.8.2/opendoas-6.8.2.tar.xz\", \"extra_sources\": [], \"description\": \"Doas allows a normal user to gain root privileges\", \"build_script\": [\"sond\"]}"


def test_pkgbuild():
    print("Reading from file:")
    pkg_build = packagebuild.package_build.from_file("package.bpb")
    
    print("Real version:")
    print(pkg_build.real_version)

    print("\n\nPKG_BUILD:")
    print(pkg_build.__dict__)
    print("\n\n")

    json_pkg_build = pkg_build.get_json()
    
    print("\n\nJSON_PKG_BUILD:")
    print(json_pkg_build)
    print("\n\n")
    
    print("PARSED DEPENDENCIES ARE:")
    for p in pkg_build.dependencies:
        print(p)

    print("WRITING BUILD FILE...")
    if(os.path.exists("new.bpb")):
        os.remove("new.bpb")

    pkg_build.write_build_file("new.bpb")

    print("CHECK: is_valid()")
    print(pkg_build.is_valid())
    print("\n")
    
    print("Testing json")
    pkg_build2 = packagebuild.package_build.from_json(SAMPLE_JSON)

    print("CHECK: is_valid()")
    print(pkg_build2.is_valid())
    print("\n")
 
    print("CHECK: as string")
    print(pkg_build2.get_string())


def test_leaf_pkg():
    lf = leafpkg.leafpkg()


    lf.name = "Sond"
    lf.version = "Hirn"
    lf.real_version = "Sondig"
    lf.description = "lol"
    lf.dependencies = "[Sond]"
   
    print(lf.__dict__)
    
    print("Writing package directory..")
    new_dir = lf.write_package_directory()
    print("DATA dir is: {}".format(new_dir))
        

    print("Creating tar..")
    lf.create_tar_package(".")
    
test_pkgbuild()
#test_leaf_pkg()
