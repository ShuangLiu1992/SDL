from conan import ConanFile
import conan.tools.files
from conan.tools.system.package_manager import Apt
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os


class SDLConan(ConanFile):
    name = "sdl"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libxext-dev"])

    def export_sources(self):
        conan.tools.files.copy(self, "*", self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os == "Macos":
            tc.variables["SDL_OPENGLES"] = False
            tc.variables["SDL_FILE"] = True
        tc.variables["SDL2_DISABLE_SDL2MAIN"] = True
        tc.variables["SDL_STATIC_PIC"] = self.options.fPIC
        tc.variables["SDL_CMAKE_DEBUG_POSTFIX"] = ""
        tc.variables["SDL_LIBC"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        if self.settings.os == "Windows":
            self.cpp_info.builddirs.append("cmake")
        else:
            self.cpp_info.builddirs.append(os.path.join("lib", "cmake"))
        self.cpp_info.set_property("cmake_file_name", "SDL2")
        self.cpp_info.set_property("cmake_target_name", "SDL2::SDL2-static")
