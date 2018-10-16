const express = require('express')
const path = require('path')

const app = express()
const port = process.env.PORT || 3000

app.set('view engine', 'pug')
app.locals.basedir = __dirname

app.listen(port, () => {
  console.log(`Listening on port ${port}.`)
})

let data = {
  options: {
    enabled: false,
    frequency: '*/15 * * * *'
  },
  account: {
    consumerKey: '',
    consumerSecret: '',
    accessToken: '',
    accessTokenSecret: ''
  },
  modules: {
    'seek-and-retweet': {
      enabled: false,
      sources: [

      ]
    }
  }
}

app.get('/', (req, res) => {
  res.render('home', {
    breadcrumbs: ['Home'],
    data: data
  })
})

app.get('/seek-and-retweet', (req, res) => {
  res.render('seek-and-retweet', {
    breadcrumbs: ['Home', 'Seek and Retweet'],
    data: data.modules['seek-and-retweet']
  })
})
