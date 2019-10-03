/* eslint-disable radix */
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const StyleLintPlugin = require('stylelint-webpack-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const WebpackNotifierPlugin = require('webpack-notifier');

const django_ip = process.env.DJANGO_IP || '127.0.0.1';
const django_port = parseInt(process.env.DJANGO_PORT || 8000);
const browsersync_port = parseInt(process.env.BROWSERSYNC_PORT || django_port + 1);
const browsersyncui_port = browsersync_port + 1;
const config = {
    entry: {
        main: ['./static/src/js/index.jsx'],
        styles: ['./static/src/scss/styles.scss'],
        nav: ['./static/src/js/nav.js'],
        home: [
            '@babel/polyfill',
            './static/src/js/index.jsx',
            './static/src/js/home.js',
            './static/src/scss/styles.scss'
        ],
        forms: [
            '@babel/polyfill',
            './static/src/js/forms/forms.jsx',
            './static/src/js/forms/tags.js',
            './static/src/js/forms/privacy.js'
        ],
        resource: ['@babel/polyfill', './static/src/js/resource/resource_detail.js']
    },
    output: {
        path: path.resolve('./static/dist/'),
        filename: 'js/[name].js'
    }
};

require('es6-promise').polyfill();

module.exports = [
    // Development webpack config
    {
        name: 'development',
        entry: config.entry,
        output: config.output,
        plugins: [
            // Set css name
            new ExtractTextPlugin({
                filename: 'css/[name].css'
            }),

            // Stylelint plugin
            new StyleLintPlugin({
                configFile: '.stylelintrc',
                context: '',
                files: '/static/src/scss/**/*.scss',
                syntax: 'scss',
                failOnError: false,
                quiet: false
            }),

            // BrowserSync
            new BrowserSyncPlugin(
                {
                    host: django_ip,
                    port: browsersync_port,
                    injectCss: true,
                    logLevel: 'silent',
                    files: ['./static/dist/css/*.css', './static/dist/js/*.js'],
                    ui: {
                        port: browsersyncui_port
                    }
                },
                {
                    reload: false
                }
            ),

            new WebpackNotifierPlugin()
        ],

        module: {
            rules: [
                {
                    enforce: 'pre',
                    test: /\.(js)$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'eslint-loader',
                        options: {
                            configFile: path.resolve('.eslintrc.js'),
                            fix: true
                        }
                    }
                },
                {
                    test: /\.(png|jpg|woff|woff2|eot|ttf|svg|otf)$/,
                    loader: 'url-loader',
                    exclude: /node_modules/
                },
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['babel-preset-env', 'react']
                        }
                    }
                },
                {
                    test: /\.scss$/,
                    exclude: /node_modules/,
                    use: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: ['css-loader', 'postcss-loader', 'sass-loader']
                    })
                },
                {
                    test: /\.css$/,
                    exclude: /node_modules/,
                    loader: 'style-loader!css-loader!'
                }
            ]
        },

        stats: {
            // Colors and log settings
            colors: true,
            version: true,
            timings: true,
            assets: true,
            chunks: false,
            source: true,
            errors: true,
            errorDetails: true,
            warnings: true,
            hash: false,
            modules: false,
            reasons: false,
            children: false,
            publicPath: false
        },

        // Create Sourcemaps for the files
        devtool: 'source-map',

        resolve: {
            alias: {
                vue: 'vue/dist/vue.js'
            }
        }
    },
    // Production webpack config
    {
        name: 'production',
        entry: config.entry,
        output: config.output,

        plugins: [
            // Specify the resulting CSS filename
            new ExtractTextPlugin({
                filename: 'css/[name].css'
            }),

            // Stylelint plugin
            new StyleLintPlugin({
                configFile: '.stylelintrc',
                context: '',
                files: '/static/src/scss/**/*.scss',
                syntax: 'scss',
                failOnError: false,
                quiet: false
            })
        ],

        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['babel-preset-env', 'react']
                        }
                    }
                },
                {
                    test: /\.(png|jpg|woff|woff2|eot|ttf|svg|otf)$/,
                    loader: 'url-loader',
                    exclude: /node_modules/
                },
                {
                    test: /\.scss$/,
                    use: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: ['css-loader', 'postcss-loader', 'sass-loader']
                    })
                }
            ]
        }
    }
];
