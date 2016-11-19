var PROD = JSON.parse(process.env.PROD_ENV || '0');

var webpack = require('webpack');
var LessPluginCleanCSS = require('less-plugin-clean-css');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var plugins = [new ExtractTextPlugin('styles.css')];
if (PROD) {
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
        filename: PROD ? 'bundle.min.js' : 'bundle.js'
    },

    devServer: {
        inline: true,
        port: 8080,
        contentBase: __dirname + '/public/'
    },

    plugins: plugins,

    module: {
        loaders: [{
            test: /\.less$/,
            // loader: "style-loader!css-loader!less-loader"
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
