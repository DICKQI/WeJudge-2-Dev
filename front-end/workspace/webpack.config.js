/**
 * Created by lancelrq on 2017/7/29.
 */
var webpack = require('webpack');
var path = require('path');
var GenerateAssetPlugin = require('generate-asset-webpack-plugin');

var createJson = function(compilation) {
    return JSON.stringify({hash: compilation.hash});
};

module.exports = {
    //页面入口文件配置
    entry: {
        index: './wejudge/index.js'
    },
    //入口文件输出配置
    output: {
        path: path.resolve('../../server/static/assets/wejudge/'),
        filename: 'app.js'
    },
    module: {
        //加载器配置
        loaders: [
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.js$/,
                loader: 'jsx-loader?harmony'
            },
            {
                test: /\.(png|jpg)$/,
                loader: 'url-loader?limit=8192'
            },
            {
                test: /\.js|jsx$/,
                loaders: ['react-hot', 'babel?presets[]=es2015,presets[]=react,presets[]=stage-0'],
                include: path.join(__dirname, 'js')
            }
        ]
    },
    //其它解决方案配置
    resolve: {
        root: path.resolve('./wejudge'),
        extensions: ['', '.js', '.json', '.scss']
    },
    //插件项
    plugins: [
        new GenerateAssetPlugin({
            filename: '../../../config/assets.json',
            fn: function(compilation, cb) {
                cb(null, createJson(compilation));
            },
            extraFiles: []
        }),
        // new (require("babili-webpack-plugin"))(),
        //new webpack.HotModuleReplacementPlugin(),
    ]
};