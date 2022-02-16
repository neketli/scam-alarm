const Express =  require('express');
const config = require('config');
const hbs = require('express-handlebars');
const multer  = require("multer");
const fs = require('fs');

const crypto  = require('crypto');

const path = require('path');


const PORT = config.get('PORT') || 8080;

const app = Express();

const CSVUtils = require('./utils/csvUtils');
const valuer = require('./utils/valuer');

app.use(Express.json())


const storageConfig = multer.diskStorage({
  destination: (req, file, cb) =>{
    cb(null, path.join(__dirname, "TMP_DATA"));
  },
  filename: (req, file, cb) =>{
    cb(null, crypto.randomBytes(16).toString("hex"));
  }
});
// определение фильтра
const fileFilter = (req, file, cb) => {
  if(file.mimetype === "text/csv" || file.mimetype === "application/vnd.ms-excel") {
    cb(null, true);
  }
  else{
    cb(null, false);
  }
}

const upload = multer({storage: storageConfig, fileFilter: fileFilter}).single("filedata");

app.use(Express.static('public'));

app.get('/', (req, res) => {
  res.status(200).sendFile('/public/index.html');
})

app.post('/api/rate/one', async (req, res) => {
  try {
    console.log(req.body)

    if(!req.body.domain){
      throw "No domain"
    }

    let domain = req.body.domain.replace('https://', '');
    domain = domain.replace('www.', '');

    res.status(200).send({ratio: await valuer.value(domain.toLowerCase())});
  }catch (e){
    res.status(500).send({"error": e});
  }
})

app.post('/api/rate/file',  upload, async (req, res) => {
  const csvValueHandler = (filedata) => {
    return new Promise(async (resolve, reject) => {
      try {
        if (!filedata) {
          reject("Invalid file!");
        }

        const fileContent = fs.readFileSync(filedata.path, "utf8");
        let domainsArray = [];
        fs.readFileSync(filedata.path, 'utf-8').split(/\r?\n/).forEach(function(line) {
          domainsArray.push(line);
        });

        const outJSON = {};

        await Promise.all(domainsArray.map(async (domain) => {
          const value = await valuer.value(domain.toLowerCase());
          outJSON[domain] = value
        }))

        resolve(outJSON);

      }catch (e){
        reject(e);
      }
    })
  }

  let fileinfo = req.file;

  try {
    const ans = await csvValueHandler(fileinfo);
    res.send(await ans);
    fs.unlink(fileinfo.path, (err) => {
      if (err) throw err
    })
  }catch (e){
    res.status(500).send({"error": e});
  }


})
app.listen(PORT);

