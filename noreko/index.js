const AWS = require('aws-sdk')
const fs = require('fs')
const {promisify} = require('util')

let image_path = "../images/frame.jpg"
const readFile = promisify(fs.readFile)
let reko = new AWS.Rekognition({
    region:'eu-west-1'
})

const readImage = async ()=>{
    try{
        let data = await readFile(image_path)
        let buf = Buffer.from(data)
        var params = {
            Image: {
                Bytes: buf
            }
        }
        reko.detectLabels(params,(err, data)=>{
            if(err)
                console.log(err)
            else
                console.log(data)
        })
    }catch(err){
        console.log(err)
    }
}

readImage()



