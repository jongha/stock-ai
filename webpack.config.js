var PRODUCTION = JSON.parse(process.env.PRODUCTION || '0');

var webpack = require('webpack');
var LessPluginCleanCSS = require('less-plugin-clean-css');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var plugins = [new ExtractTextPlugin('styles.css')];
if (PRODUCTION) {
    plugins.push(new webpack.optimize.UglifyJsPlugin({
        compress: {
            warnings: false,
        },
        output: {
            comments: false
        }
    }));
}

module.exports = {
    entry: './src/index.js',

    devtool: 'source-map',

    output: {
        path: __dirname + '/static/',
        filename: PRODUCTION ? 'bundle.min.js' : 'bundle.js'
    },

    devServer: {
        inline: true,
        port: 8080,
        contentBase: __dirname + '/public/'
    },

    plugins: plugins,

    module: {
        lessLoader: {
            lessPlugins: [
                new LessPluginCleanCSS({
                    advanced: true
                })
            ]
        },
        loaders: [{
            test: /\.css$/,
            loader: ExtractTextPlugin.extract(
                'css-loader?sourceMap!'
            )
        }, {
            test: /\.less$/,
            loader: ExtractTextPlugin.extract(
                'css-loader?sourceMap!' +
                'less-loader?sourceMap'
            )
        }, {
            test: /\.js$/,
            loader: 'babel',
            exclude: /node_modules/,
            query: {
                cacheDirectory: true,
                presets: ['es2015', 'react']
            }
        }]
    }
};
