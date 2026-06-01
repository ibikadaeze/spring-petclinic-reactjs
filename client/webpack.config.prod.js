const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    entry: './src/main.tsx', // Your true entry point file path
    output: {
        path: path.join(__dirname, 'public', 'dist'),
        filename: 'bundle.js',
        publicPath: '/dist/'
    },
    resolve: {
        extensions: ['.js', '.ts', '.tsx'] 
    },
    resolveLoader: {
        modules: ['node_modules']
    },
    module: {
        rules: [
            // COMMENTED OUT OR REMOVED TSLINT-LOADER TO PREVENT THE VERSION CRASH
            /*
            {
                test: /\.tsx?$/,
                enforce: 'pre', 
                loader: 'tslint-loader'
            },
            */
            {
                test: /\.tsx?$/,
                loader: 'ts-loader',
                exclude: /node_modules/
                options: {
                    transpileOnly: true
                }
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader'
                })
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        // You can leave the rest of the plugins array untouched
        new ExtractTextPlugin('styles.css')
    ]
};
