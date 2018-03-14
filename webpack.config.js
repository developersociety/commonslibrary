const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const webpackPort = parseInt(process.env.WEBPACK_PORT || 3000);

module.exports = {
  context: __dirname,

  entry: {
    main: [
        'webpack-dev-server/client?http://127.0.0.1:' + webpackPort + '/',
        './static/src/js/index',
        './static/src/scss/styles.scss'
    ],
    registration: [
        'webpack-dev-server/client?http://127.0.0.1:' + webpackPort + '/',
        './static/src/js/form'
    ]
  },

  output: {
    path: path.resolve('./static/bundles/'),
    filename: "[name].js",
    publicPath: 'http://127.0.0.1:' + webpackPort + '/static/bundles/'
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin({
      filename: 'css/[name].css',
      allChunks: true,
    })
  ],

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
      {
        test: /\.css$/,
        exclude: '/node_modules/',
        loader: ExtractTextPlugin.extract({
          use: ['css-loader?importLoaders=1'],
        })
      },
      {
        test: /\.scss$/,
        exclude: '/node_modules/',
        loader: ExtractTextPlugin.extract([
          'css-loader',
          'sass-loader'
        ])
      },
      {
        test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
        loader: 'file-loader',
        options: {
          name: 'assets/[name].[ext]'
        }
      }
    ]
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  }
}
