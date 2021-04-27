const { Resolver } = require('dns')
const resolver = new Resolver();
resolver.setServers(['192.168.50.2']);
const express = require('express')
const app = express()
const port = 53535
const fs = require('fs')
const https = require('https')

app.get('/',(req,res) => {
	let domain = req.query.domain;
	//res.send(`hello world ${domain}` )
	
	res.header('Access-Control-Allow-Origin','*');
	console.log(`domain: ${domain}`)
	res.end('OK')
	resolver.resolve4(domain, (err,address)=>{
		//res.end(`${domain} address is ${address}` )
	})
})

https.createServer({
	key:fs.readFileSync('/var/cert/new/server.key'),
	cert:fs.readFileSync('/var/cert/new/server.crt')
},app).listen(port,() => {
	console.log(`listen on ${port}`)
})
