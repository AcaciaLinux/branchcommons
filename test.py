import unittest
from src import packagebuild

SAMPLE_JSON = "{\"name\": \"doas\", \"version\": \"6.8.2\", \"real_version\": \"0\", \"dependencies\": [\"linux-pam\"], \"build_dependencies\": [\"linux-pam\", \"bash\", \"autoconf\", \"shadow\"], \"cross_dependencies\": [], \"source\": \"https://github.com/Duncaen/OpenDoas/releases/download/v6.8.2/opendoas-6.8.2.tar.xz\", \"extra_sources\": [], \"description\": \"Doas allows a normal user to gain root privileges\", \"build_script\": [\"sond\"]}"

class TestPackageBuild(unittest.TestCase):
    
    def test_file_read(self):
        """
        Check: from_file returns a valid pkgbuild for valid input.
        """
        pkg_build = packagebuild.package_build.from_file("testfiles/package.bpb")
        self.assertEqual(pkg_build.is_valid(), True)
    
    def test_read_write(self):
        """
        Check: assert parsed = written file  
        """
        pkg_build = packagebuild.package_build.from_file("testfiles/package.bpb")
        pkg_build.write_build_file("testfiles/new.bpb")

        with open("testfiles/package.bpb", "rb") as file_orig:
            with open("testfiles/new.bpb", "rb") as file_new:
                self.assertEqual(file_orig.read(), file_new.read())

    def test_invalid_file(self):
        """
        Check: from_file on an invalid pkgbuild return is_valid False
        """
        pkg_build = packagebuild.package_build.from_file("testfiles/invalid.bpb")
        self.assertEqual(pkg_build.is_valid(), False)

    def test_json(self):
        """
        Check: valid json produces valid packagebuild
        """
        pkg_build = packagebuild.package_build.from_json(SAMPLE_JSON)
        self.assertEqual(pkg_build.is_valid(), True)


if __name__ == '__main__':
    unittest.main()

