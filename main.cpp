#include <InSDL/InSDL.hpp>

int main() {
    insdl::App app;
    app.init(800, 600, "My InSDL App");

    while (!app.quit) {
        insdl::handleEvent(app);

        app.update();
    }

    return 0;
}