const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

// TODO: Take the value passed down by gulp.
const devMode = process.env.NODE_ENV !== 'production';

const config = {
  entry:  __dirname + '/src/js/index.jsx',
  output: {
    path: path.resolve(__dirname, 'src', 'static'),
    filename: 'bundle.js',
  },
  resolve: {
    extensions: ['.js', '.jsx', '.scss']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: path.resolve(__dirname, 'src', 'node_modules'),
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.s(a|c)ss$/,
        use: [
          {
            loader: devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
            options: {
              modules: true,
              localIdentName: devMode ? '[local]' : '[name]__[local]__[hash:base64:5]',
              camelCase: 'dashes',
            }
          },
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
                path.resolve(__dirname, 'src', 'sass')
              ]
            }
          }, 
        ]
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'style.css',
    }),
  ]
};
module.exports = config;
