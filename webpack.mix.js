let mix = require('laravel-mix');


mix.browserSync({
    proxy: "127.0.0.1:8000/UI",
    files: ["UI/**"]
});
