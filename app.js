const express = require('express')
//const exphbs = require('express-handlebars')

const PORT = process.env.PORT  || 3000

const app = express()
// const hbs = exphbs.create({
// 	defaultLayout: 'main',
// 	extname: 'hbs'
// })

// app.engine('hbs', hbs.engine)
// app.set('view engine', 'hbs')
// app.set('views', 'views')

async function start() {
	try {		
	app.listen(PORT, () => {
		console.log('Server has been started...');
	})
	} catch (err) {
		console.log(err);
	}
}

start()