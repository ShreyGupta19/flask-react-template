const path = require('path');
const merge = require('webpack-merge');
const baseConfig = require('./webpack.base.js');

const config = merge.strategy(
  {
    'module.rules.use': 'prepend',   
  }
)({
  mode: 'development',
  output: {
    path: path.resolve(__dirname, '..', 'src', 'static'),
  },
  module: {
    rules: [
      {
        test: /\.s(a|c)ss$/,
        use: [
          {
            loader: 'style-loader',
          },
          {
            loader: 'css-loader',
            options: {
              modules: true,
              localIdentName: '[local]',
              camelCase: 'dashes',
            }
          },
        ]
      },
    ]
  },
}, baseConfig);

module.exports = config;
