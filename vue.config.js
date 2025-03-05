
module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
    ? '/pytheas-db/'
    : '/',
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

