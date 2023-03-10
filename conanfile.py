from conans import ConanFile, CMake, tools


class MatioCppConan(ConanFile):
    name = "matio-cpp"
    version = "0.21"
    license = "BSD 2-Clause"
    author = "Yury Lunev <yury.lunev@gmail.com>"
    url = "https://github.com/koolkhel/matio-cpp-recipe"
    description = "C++ wrapper for Matio library"
    topics = ("matlab", "cpp")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    requires = "matio/1.5.23"
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/ami-iit/matio-cpp.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("matio-cpp/CMakeLists.txt", "project(matioCpp VERSION 0.2.1 LANGUAGES CXX)",
                              '''project(MatioCpp VERSION 0.2.1 LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="matio-cpp")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="matio-cpp/include")
        self.copy("*.h", dst="include", src="Autogenerated")
        self.copy("*.tpp", dst="include", src="matio-cpp/include")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["matioCpp"]

