import tarfile
import os
import blog
import shutil

class leafpkg():
    def __init__(self):
        self.name = ""
        self.version = ""
        self.real_version = ""
        self.description = ""
        self.dependencies = ""
    
    def write_package_directory(self):
        pkg_dir = "{}-{}".format(self.name, self.version)
        pkg_path = os.path.join(os.getcwd(), pkg_dir)

        # create pkg dir
        try:
            os.mkdir(pkg_path)
        except FileExistsError:
            shutil.rmtree(pkg_path)
            os.mkdir(pkg_path)

        #create data subdir
        os.mkdir(os.path.join(pkg_path, "data"))

        leaf_pf = open(os.path.join(pkg_path, "leaf.pkg"), "w")
        leaf_pf.write("name={}\n".format(self.name))
        leaf_pf.write("version={}\n".format(self.version))
        leaf_pf.write("real_version={}\n".format(self.real_version))
        leaf_pf.write("description={}\n".format(self.description))
        leaf_pf.write("dependencies={}\n".format(self.dependencies))
        return os.path.join(pkg_path, "data")
    
    def create_tar_package(self, package_directory):
        pkg_name = "{}-{}".format(self.name, self.version)
        tar_name = "{}.lfpkg".format(pkg_name)
        pkg_file_tar = tarfile.open(os.path.join(package_directory, tar_name), "w:xz")
        
        leafpkg_dir = os.path.join(package_directory, pkg_name)
        for root, dirs, files in os.walk(leafpkg_dir, followlinks=False):
            for file in files:
                blog.info("Adding file: {}".format(os.path.join(root, file)))
                pkg_file_tar.add(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(leafpkg_dir, '..')))
            for dir in dirs:
                if (len(os.listdir(os.path.join(root, dir))) == 0):
                    blog.info("Adding dir: {}".format(os.path.join(root, dir)))
                    pkg_file_tar.add(os.path.join(root, dir), os.path.relpath(os.path.join(root, dir), os.path.join(leafpkg_dir, '..')))
                elif (os.path.islink(os.path.join(root, dir))):
                    blog.info("Adding dirlink: {}".format(os.path.join(root, dir)))
                    pkg_file_tar.add(os.path.join(root, dir), os.path.relpath(os.path.join(root, dir), os.path.join(leafpkg_dir, '..')))

        pkg_file_tar.close()
        blog.info("Package file created in {}".format(package_directory))
        return os.path.join(package_directory, tar_name)
