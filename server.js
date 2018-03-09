'use strict';

const Webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const webpackConfig = require('./webpack.config');
const compiler = Webpack(webpackConfig);

const webpackPort = parseInt(process.env.WEBPACK_PORT || 3000);


const server = new WebpackDevServer(compiler, {
  inline: true,
  noInfo: true,
  publicPath: webpackConfig.output.publicPath,
  headers: {
    "Access-Control-Allow-Origin": "*",
  }
});

server.listen(webpackPort, '127.0.0.1', () => {
  console.log('Starting server on 127.0.0.1:' + webpackPort);
});
