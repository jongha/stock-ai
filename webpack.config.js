module.exports = {
    entry: './src/index.js',

    output: {
        path: __dirname + '/static/',
        filename: 'bundle.js'
    },

    devServer: {
        inline: true,
        port: 8080,
        contentBase: __dirname + '/public/'
    },

    module: {
        loaders: [{
            test: /\.css$/,
            loader: "style!css"
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