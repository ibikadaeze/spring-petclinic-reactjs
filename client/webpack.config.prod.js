const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    mode: 'production', // Explicitly set for modern Webpack engines
    entry: './src/index.tsx', // Adjust to your actual entry path if different
    output: {
        path: path.join(__dirname, 'public', 'dist'),
        filename: 'bundle.js',
        publicPath: '/dist/'
    },
    resolve: {
        // FIXED: Removed the empty string "" from extensions array
        extensions: ['.js', '.ts', '.tsx'] 
    },
    resolveLoader: {
        // FIXED: Removed the obsolete 'fallback' property entirely
        modules: ['node_modules']
    },
    module: {
        // FIXED: Merged 'preLoaders' and 'loaders' into modern 'rules'
        rules: [
            {
                test: /\.tsx?$/,
                enforce: 'pre', // Converts 'preLoaders' logic safely
                loader: 'tslint-loader'
            },
            {
                test: /\.tsx?$/,
                loader: 'ts-loader',
                exclude: /node_modules/
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
        // FIXED: Wrapped custom legacy properties into LoaderOptionsPlugin
        new webpack.LoaderOptionsPlugin({
            options: {
                tslint: {
                    emitErrors: true,
                    failOnHint: true
                }
            }
        }),
        new ExtractTextPlugin('styles.css')
    ]
};
