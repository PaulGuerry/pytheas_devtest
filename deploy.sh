#!/usr/bin/env sh

# abort on errors
set -e

# build
<<<<<<< HEAD
pnpm run build
=======
npm run build
>>>>>>> e5809672622a4ac99f3f3368870f01e26ccbcb86

# navigate into the build output directory
cd dist

# if you are deploying to a custom domain
<<<<<<< HEAD
echo 'pytheasdb.com' > CNAME
=======
# echo 'www.example.com' > CNAME
>>>>>>> e5809672622a4ac99f3f3368870f01e26ccbcb86

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io
# git push -f git@github.com:<USERNAME>/<USERNAME>.github.io.git main

# if you are deploying to https://<USERNAME>.github.io/<REPO>
# git push -f git@github.com:<USERNAME>/<REPO>.git main:gh-pages
<<<<<<< HEAD
git push -f git@github.com:PaulGuerry/pytheas-db.git main:gh-pages
=======
git push -f git@github.com:PaulGuerry/13_vue_computed-property.git main:gh-pages
>>>>>>> e5809672622a4ac99f3f3368870f01e26ccbcb86

cd -
