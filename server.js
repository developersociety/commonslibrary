'use strict';

const Webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const webpackConfig = require('./webpack.config');

const compiler = Webpack(webpackConfig);

const server = new WebpackDevServer(compiler, {
  inline: true,
  publicPath: webpackConfig.output.publicPath
});

server.listen(8080, '127.0.0.1', () => {
  console.log('Starting server on 127.0.0.1:8080');
});
