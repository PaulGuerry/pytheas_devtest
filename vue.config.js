
module.exports = {
  publicPath: '/',
  configureWebpack: {
        module: {
            rules: [ // proper handle of .mjs files
                {
                    type: 'javascript/auto',
                    test: /\.mjs$/,
                    loader: 'babel-loader'
                }
            ]
        }
    }
}

