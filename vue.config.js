
module.exports = {
<<<<<<< HEAD
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
=======
  publicPath: process.env.NODE_ENV === 'production'
    ? '/13_devtest/'
    : '/'
>>>>>>> e5809672622a4ac99f3f3368870f01e26ccbcb86
}

