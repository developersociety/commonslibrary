const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: [
    'webpack-dev-server/client?http://127.0.0.1:8080/',
    './static/js/index'
  ],

  output: {
      path: path.resolve('./static/bundles/'),
      filename: "[name].js",
      publicPath: 'http://127.0.0.1:8080/static/bundles/'
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      }
    ]
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  }
}
