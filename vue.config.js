
module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
    ? '/pytheas_devtest/'
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

