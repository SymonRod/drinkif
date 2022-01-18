
const path = require('path');

module.exports = {
    // Should be STATIC_URL + path/to/build
    publicPath: 'static/',

    // Output to a directory in STATICFILES_DIRS
    outputDir: path.resolve(__dirname, '../backend/drinkif/static'),

    // Django will hash file names, not webpack
    filenameHashing: true,

    // See: https://vuejs.org/v2/guide/installation.html#Runtime-Compiler-vs-Runtime-only
    runtimeCompiler: true,

    devServer: {
        writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
    },

    pwa: {
        name: 'Drinkif',
        themeColor: '#00bad3',
        msTileColor: '#000000',
        appleMobileWebAppCapable: 'yes',
        appleMobileWebAppStatusBarStyle: 'black',
        display: 'fullscreen',

        // configure the workbox plugin
        workboxPluginMode: 'GenerateSW',
        // workboxPluginMode: 'InjectManifest',
        // workboxOptions: {
        //     // swSrc is required in InjectManifest mode.
        //   swSrc: 'src/registerServiceWorker.js',
        //     // ...other Workbox options...
        // }
    },

    pluginOptions: {
      i18n: {
        locale: 'en',
        fallbackLocale: 'en',
        localeDir: 'locales',
        enableLegacy: false,
        runtimeOnly: false,
        compositionOnly: false,
        fullInstall: true
      }
    }
};