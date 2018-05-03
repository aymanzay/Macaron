var express = require('express')
var app = express()
var path = require('path')
var port = 3000;
var fs = require('fs')
var bodyParser = require('body-parser')


//all files
const stage1 = "arrays.txt"
const stage2 = "middle.txt"
const stage3 = "translated.txt"

//global variables
var vectors = []


var files = fs.readdirSync('public/assets/')
var path = []


//Execute python code to classify all elements and save output to file
/*
//Stage 1: classify all songs in files list and return arrays.txt contatining the classified arrays 
var python = require('child_process').spawn('python', ["python/classify.py classify"])

python.on('close', function(code) {
  if(code !== 0) {
    console.log("error")
  }
})
*/

//save vectors into application to send to client onload
fs.readFile(stage1, "utf8", function(err, data) {
  var arrays = data.toString().split("[")
  var tempArr = []
  arrays.splice(0,1) //to get rid of initial empty element
  arrays.forEach(function(item) {
    item = item.split()
    item.forEach(function(x) {
      x = x.split("   ")
      x.forEach(function(y) {
        tempArr.push(y.trim())
      })
      vectors.push(tempArr)
      tempArr = []
    })
  })
})

//Stage 2: Allowing enough time to populate vectors variable before
//writing them to middle.txt
setTimeout(function(){ 
  fs.writeFile(stage2,vectors, function(err) {
    if(err) {
      return console.log(err)
    }
    console.log("saved")
  })
  
}, 2000);
//Executing python script for kNN classification to generate playlist

//want a settimeout function here
/*
var translated = "translated.txt"
var returning = []
fs.readFile(translated, "utf8", function(err, data) {
  var arrays = data.toString().split("[")
  var tempArr = []
  arrays.splice(0,1)
  arrays.forEach(function(item) {
    item = item.split()
    item.forEach(function(x) {
      x = x.split("   ")
      x.forEach(function(y) {
        tempArr.push(y.trim())
      })
      returning.push(tempArr)
      tempArr = []
    })
  })
  console.log(returning)
  console.log("second save")
})
*/

//Creating library list
files.forEach(function(file) {
  if(!file.endsWith('.mp3')){
    files.splice(0,1)
  }
})

files.forEach(function(file) {
  path.push('assets/'.concat("", file))
})

var leng = path.length

//Application Handling
var data = files.map( function(x, i, j){
  return {"fileList": x, "paths": path[i], "vectors": vectors[i]}        
}.bind(this));

app.set('view engine', 'ejs')

//middleware
urlencParser = bodyParser.urlencoded({extended: false})
app.use(express.static('public'));
app.use(bodyParser.json());

app.get('/', function (req, res, next) {
  res.render('index.ejs', {
    title: "Macaron Demo",
    lib: data,
    libLen: leng
  })
})

app.post('/', urlencParser, function(req, res, next) {
  var index = req.body.target_song
  var command = "python/classify.py generate "+index

  //spawn python process
  var pykNN = require('child_process').spawn('python', [command]) //plus an index given by user
  pykNN.stdout.on('data',function(chunk){
    var textChunk = chunk.toString('utf8');// buffer to string
    util.log(textChunk);
  })
  console.log("python returned")
  //parse translated arrays to 2d
  var recom = []
  fs.readFile(stage3, "utf8", function(err, data) {
    var arrays = data.toString().split("[")
    var tempArr = []
    arrays.splice(0,1)
    arrays.forEach(function(item) {
      item = item.split()
      item.forEach(function(x) {
        x = x.split("   ")
        x.forEach(function(y) {
          y = y.replace(/(\r\n|\n|\r)/gm,"");
          y = y.replace("]", "")
          tempArr.push(y.trim())
        })
        recom.push(tempArr)
        tempArr = []
      })
    })
  })

  setTimeout(function(){
    var data = files.map( function(x, i){
      return {"fileList": x, "paths": path[i], "vectors": vectors[i]}        
    }.bind(this));

    //Used to help parsing in client-side
    var genlen = recom.length //genlen = k from kNN

    res.render('generate-success', {
      title: "Macaron Demo",
      lib: data,
      libLen: leng,
      generated: recom,
      gLen: genlen
    })
  }, 2000);
})

app.listen(port, function() {
  console.log('Listening on port 3000!')
})

