import packagebuild
import leafpkg

import os

SAMPLE_JSON = "{\"name\": \"iproute2\", \"version\": \"5.19.0\", \"real_version\": \"0\", \"dependencies\": \"[glibc][libelf]\", \"build_dependencies\": \"[glibc][libelf][flex][bison][findutils]\", \"cross_dependencies\": \"\", \"source\": \"https://www.kernel.org/pub/linux/utils/net/iproute2/iproute2-5.19.0.tar.xz\", \"extra_sources\": [], \"description\": \"\", \"build_script\": [\"cd $PKG_NAME-$PKG_VERSION\", \"sed -i /ARPD/d Makefile\", \"rm -fv man/man8/arpd.8\", \"make -j$(nproc) NETNS_RUN_DIR=/run/netns\", \"make DESTDIR=$PKG_INSTALL_DIR SBINDIR=/usr/sbin install\", \"rm -fv $PKG_INSTALL_DIR/usr/share/info/dir\"]}"

def test_pkgbuild():
    pkg_build = packagebuild.package_build.from_file("package.bpb")
    
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
test_leaf_pkg()
