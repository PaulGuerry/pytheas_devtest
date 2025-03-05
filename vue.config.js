
module.exports = {
<<<<<<< HEAD
<<<<<<< HEAD
  publicPath: '/',
||||||| c62896b7
  publicPath: '/',
=======
    publicPath: process.env.NODE_ENV === 'production'
    ? '/pytheas_devtest/'
    : '/',
>>>>>>> ddd44671570fbe9ec745f9aa2f0f6db7a89c9468
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

