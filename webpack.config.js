const path = require('path');

module.exports = {
    devtool:'eval-source-map',
    entry: {
        index: './src/index.js',
        result: './src/result.js'
    },
    output: {
        filename: '[name]-[hash].js',
        path:  __dirname + '/build'
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.js$/,
                loader: 'ify-loader'
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: [
                    'file-loader'
                ]
            }
        ]
    }
};