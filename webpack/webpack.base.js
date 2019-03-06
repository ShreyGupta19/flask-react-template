const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const basePath = path.resolve(__dirname, '..', 'src/');

const config = {
  context: basePath,
  entry: {
    'index': './js/index.jsx',
    'login': './js/login.js',
  }, 
  output: {
    filename: '[name].js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.scss']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: path.resolve(basePath, '..', 'node_modules'),
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.s(a|c)ss$/,
        use: [
          {
            loader: 'postcss-loader',
            options: {
              plugins: function () {
                return [
                  require('precss'),
                  require('autoprefixer')
                ];
              }
            }
          },
          {
            loader: 'sass-loader',
            options: {
              includePaths: [
                path.resolve('sass')
              ]
            }
          }, 
        ]
      },
    ]
  },
};

module.exports = config;
