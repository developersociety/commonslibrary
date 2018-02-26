const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: [
    'webpack-dev-server/client?http://127.0.0.1:8080/',
    './static/js/index',
    './static/scss/styles.scss'
  ],

  output: {
      path: path.resolve('./static/bundles/'),
      filename: "[name].js",
      publicPath: 'http://127.0.0.1:8080/static/bundles/'
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin({
      filename: 'static/css/[name].css',
      allChunks: true,
    })
  ],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
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
          'css-loader?url=false',
          'sass-loader'
        ])
      }
    ]
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  }
}
