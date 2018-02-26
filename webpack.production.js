const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: [
    './static/src/js/index',
    './static/src/scss/styles.scss'
  ],

  output: {
    path: path.resolve('./static/dist/'),
    filename: "[name].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-production-stats.json'}),
    new webpack.optimize.UglifyJsPlugin(),
    new ExtractTextPlugin({
      filename: 'css/[name].css',
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
          use: ['css-loader?importLoaders=1!minimize', 'postcss-loader'],
        })
      },
      {
        test: /\.scss$/,
        exclude: '/node_modules/',
        loader: ExtractTextPlugin.extract([
          'css-loader?url=false',
          'sass-loader',
          'postcss-loader'
        ])
      }
    ]
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx']
  }
}
