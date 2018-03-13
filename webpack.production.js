const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: {
    main: [
        './static/src/js/index',
        './static/src/scss/styles.scss'
    ],
    form: [
        './static/src/js/form',
    ]
  },

  output: {
    path: path.resolve('./static/dist/'),
    filename: "[name].js"
  },

  plugins: [
    new BundleTracker({filename: './webpack-production-stats.json'}),
    new webpack.optimize.UglifyJsPlugin(),
    new ExtractTextPlugin({
      filename: '[name].css',
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
